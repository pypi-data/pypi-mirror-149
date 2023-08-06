from pydantic import BaseModel, Field
from pydantic.json import pydantic_encoder

from locatieserver.schema.free import FreeResponse
from locatieserver.schema.lookup import LookupResponse
from locatieserver.schema.suggest import SuggestResponse


class OpenAPI(BaseModel):
    suggest_response: SuggestResponse = Field(..., alias="SuggestResponse")
    free_response: FreeResponse = Field(..., alias="FreeResponse")
    lookup_response: LookupResponse = Field(..., alias="LookupResponse")


if __name__ == "__main__":

    x = OpenAPI.schema(ref_template="#/components/schemas/{model}")

    y = OpenAPI.__config__.json_dumps(x["definitions"], default=pydantic_encoder, indent=2)
    print(y)
