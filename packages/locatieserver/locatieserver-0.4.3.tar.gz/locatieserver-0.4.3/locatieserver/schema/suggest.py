from __future__ import annotations

from typing import Dict, List, Union

from pydantic import Field

from locatieserver.schema.base import LocatieserverBaseModel


class SuggestDoc(LocatieserverBaseModel):
    type: str
    weergavenaam: str
    id: str
    score: float


class SuggestInlineResponse(LocatieserverBaseModel):
    num_found: int = Field(..., alias="numFound")
    start: int
    max_score: float = Field(..., alias="maxScore")
    docs: List[SuggestDoc]


class Suggest(LocatieserverBaseModel):
    suggest: List[str]


class Suggestion(LocatieserverBaseModel):
    num_found: int = Field(..., alias="numFound")
    start_offset: int = Field(..., alias="startOffset")
    end_offset: int = Field(..., alias="endOffset")
    suggestion: List[str]


class Collation(LocatieserverBaseModel):
    collation_query: str = Field(..., alias="collationQuery")
    hits: int
    misspellings_and_corrections: List[str] = Field(..., alias="misspellingsAndCorrections")


class Spellcheck(LocatieserverBaseModel):
    suggestions: List[Union[str, Suggestion]]
    collations: List[Union[str, Collation]]


class SuggestResponse(LocatieserverBaseModel):
    """Response for the suggest service"""

    response: SuggestInlineResponse
    highlighting: Dict[str, Suggest]
    spellcheck: Spellcheck


if __name__ == "__main__":
    x = SuggestResponse.schema_json()

    print(x)
