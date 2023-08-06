"""API methods of the locatieserver grouped in this module for clean imports."""


from .free import free
from .lookup import lookup
from .suggest import suggest

__all__ = ["free", "lookup", "suggest"]
