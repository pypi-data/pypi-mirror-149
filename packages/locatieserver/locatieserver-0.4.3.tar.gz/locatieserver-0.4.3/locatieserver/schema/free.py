from __future__ import annotations

from typing import List

from pydantic import Field

from locatieserver.schema.base import LocatieserverBaseModel
from locatieserver.schema.utils import Point


class FreeDoc(LocatieserverBaseModel):
    """Free service document"""

    bron: str
    woonplaatscode: str
    type: str
    woonplaatsnaam: str
    huis_nlt: str
    openbareruimtetype: str
    gemeentecode: str
    weergavenaam: str
    straatnaam_verkort: str
    id: str
    gemeentenaam: str
    identificatie: str
    openbareruimte_id: str
    provinciecode: str
    postcode: str
    provincienaam: str
    centroide_ll: Point
    nummeraanduiding_id: str
    adresseerbaarobject_id: str
    huisnummer: int
    provincieafkorting: str
    centroide_rd: Point
    straatnaam: str
    gekoppeld_perceel: List[str]
    score: float


class FreeInlineResponse(LocatieserverBaseModel):
    num_found: int = Field(..., alias="numFound")
    start: int
    max_score: float = Field(..., alias="maxScore")
    docs: List[FreeDoc]


class FreeResponse(LocatieserverBaseModel):
    """Response for the free service"""

    response: FreeInlineResponse
