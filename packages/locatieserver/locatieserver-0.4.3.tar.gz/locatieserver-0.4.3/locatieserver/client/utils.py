import inspect
from typing import Any, Callable, Dict

import httpx

from locatieserver.client.config import BASE_URL
from locatieserver.schema.error import ErrorResponse

DEFAULT_CACHE = {}


def get_defaults_from_function(func: Callable) -> Dict[str, Any]:
    if func.__name__ not in DEFAULT_CACHE:
        signature = inspect.signature(func)
        DEFAULT_CACHE[func.__name__] = {
            k: v.default for k, v in signature.parameters.items() if v.default is not inspect.Parameter.empty
        }

    return DEFAULT_CACHE[func.__name__]


def filter_defaults(func, **kwargs):

    defaults = get_defaults_from_function(func)

    non_default_values = {}

    for key, value in kwargs.items():
        if key not in defaults or value != defaults[key]:
            non_default_values[key] = value

    return non_default_values


class LocatieserverError(Exception):
    pass


class LocatieserverResponseError(LocatieserverError):
    pass


def http_get(path, params):
    response = httpx.get(BASE_URL + path, params=params)

    content_type = response.headers.get("Content-Type", None)

    if "json" not in content_type:
        raise LocatieserverError(f"Cannot handle content-types other then JSON, received {content_type}.")

    if response.status_code == 200:
        return response
    elif response.status_code == 400:
        error_response = ErrorResponse.parse_raw(response.content)

        raise LocatieserverResponseError(error_response.error.msg)

    return response
