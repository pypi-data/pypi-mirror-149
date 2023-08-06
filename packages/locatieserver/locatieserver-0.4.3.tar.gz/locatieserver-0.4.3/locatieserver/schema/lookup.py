from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from locatieserver.schema.base import LocatieserverBaseModel
from locatieserver.schema.utils import Point


class LookupDoc(LocatieserverBaseModel):
    """Lookup service document"""

    bron: Optional[str]
    woonplaatscode: Optional[str]
    type: Optional[str]
    woonplaatsnaam: Optional[str]
    huis_nlt: Optional[str]
    openbareruimtetype: Optional[str]
    gemeentecode: Optional[str]
    weergavenaam: Optional[str]
    straatnaam_verkort: Optional[str]
    id: Optional[str]
    gemeentenaam: Optional[str]
    identificatie: Optional[str]
    openbareruimte_id: Optional[str]
    provinciecode: Optional[str]
    postcode: Optional[str]
    provincienaam: Optional[str]
    centroide_ll: Optional[Point]
    nummeraanduiding_id: Optional[str]
    adresseerbaarobject_id: Optional[str]
    huisnummer: Optional[int]
    huisnummertoevoeging: Optional[str] = ""
    huisletter: Optional[str] = ""
    provincieafkorting: Optional[str]
    centroide_rd: Optional[Point]
    straatnaam: Optional[str]
    gekoppeld_perceel: Optional[List[str]]


class LookupInlineResponse(LocatieserverBaseModel):
    num_found: int = Field(..., alias="numFound")
    start: int
    docs: List[LookupDoc]


class LookupResponse(LocatieserverBaseModel):
    """Response for the lookup service"""

    response: LookupInlineResponse
