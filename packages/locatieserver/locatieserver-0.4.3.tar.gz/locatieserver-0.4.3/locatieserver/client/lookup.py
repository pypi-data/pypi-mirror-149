from typing import Optional

from locatieserver.client.utils import filter_defaults, http_get
from locatieserver.schema.lookup import LookupResponse

PATH = "lookup"


def lookup(
    id: str,
    rows: Optional[int] = 10,
    start: Optional[int] = 0,
    wt: Optional[str] = "json",
    indent: Optional[bool] = True,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    fq: Optional[str] = "type:(gemeente OR woonplaats OR weg OR postcode OR adres)",
) -> LookupResponse:
    """Lookup Service

    For more info: https://github.com/PDOK/locatieserver/wiki/API-Locatieserver#4lookup-service

    :param id: Bij de lookup-service moet de id-parameter worden gebruikt om het ID op te geven van het object
        waar naar gezocht dient te worden. De waarde van het ID kan worden bepaald door gebruik te maken van
        de suggest-service, of deze kan uit een extern systeem komen waar dit ID eerder in is opgeslagen.
    :param rows: Hiermee wordt opgegeven wat het maximale aantal rijen (ofwel resultaten)
        is dat teruggegeven moet worden op deze bevraging.
    :param start: Hiermee wordt opgegeven wat de index is van het eerste resultaat dat teruggegeven wordt.
        Dit is zero-based. In combinatie met de rows-parameter kunnen deze services gepagineerd worden bevraagd.
    :param wt: Hiermee wordt opgegeven wat het outputformaat is van de bevraging.
    :param indent: Hiermee kan worden opgegeven of de teruggegeven JSON ingesprongen (geïndenteerd) moet worden.
    :param lat: Werkt alleen in combinatie met `lon`.
        Hiermee kan een coördinaat (in lat/lon, ofwel WGS84) worden opgegeven.
        Met behulp van deze parameters worden de gevonden zoekresultaten gesorteerd op afstand van het meegegeven punt.
        Wanneer de locatie van de gebruiker bekend is, kan op deze manier effectiever worden gezocht.
        Het meegeven van een coördinaat is met name nuttig voor de suggest- en vrije geocoder-services.
        Hier worden meestal meerdere resultaten teruggegeven.
        Als decimaal scheidingsteken moet een punt worden opgegeven i.p.v. een komma.
    :param lon: Werkt alleen in combinatie met `lat`.
        Hiermee kan een coördinaat (in lat/lon, ofwel WGS84) worden opgegeven.
        Met behulp van deze parameters worden de gevonden zoekresultaten gesorteerd op afstand van het meegegeven punt.
        Wanneer de locatie van de gebruiker bekend is, kan op deze manier effectiever worden gezocht.
        Het meegeven van een coördinaat is met name nuttig voor de suggest- en vrije geocoder-services.
        Hier worden meestal meerdere resultaten teruggegeven.
        Als decimaal scheidingsteken moet een punt worden opgegeven i.p.v. een komma.
    :param fq: Hiermee kan een filter query worden opgegeven, bijv. `fq=bron:BAG`.
        Met `fq=*` kan de default filter query worden opgeheven.
    :return: LookupResponse schema
    """
    params = filter_defaults(
        lookup,
        id=id,
        rows=rows,
        start=start,
        wt=wt,
        indent=indent,
        lat=lat,
        lon=lon,
        fq=fq,
    )

    response = http_get(PATH, params)

    return LookupResponse.parse_raw(response.content)
