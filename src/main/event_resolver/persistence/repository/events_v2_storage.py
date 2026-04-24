import logging
import re
from datetime import UTC, datetime, timedelta
from typing import cast

from SPARQLWrapper import JSON, SPARQLWrapper

from event_resolver.persistence.models.region_country_map import (
    get_country_qcodes_for_regions,
)
from event_resolver.persistence.models.wikidata_class_enum import (
    WikidataClassEnum,
)

logger = logging.getLogger(__name__)

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
SPARQL_USER_AGENT = (
    "TGPM-Backend/1.0 (https://github.com/TempoGeoPoliticalMap; contact@tgpm.org)"
)
SPARQL_TIMEOUT_SECONDS = 30

_MAIN_QUERY_TEMPLATE = """
SELECT DISTINCT
  ?item ?itemLabel ?itemType
  ?startTime ?endTime
  ?description
  ?imageUrl
  ?wikipediaUrl
  (GROUP_CONCAT(DISTINCT ?countryId;    separator="|") AS ?countryIds)
  (GROUP_CONCAT(DISTINCT ?countryLabel; separator="|") AS ?countryLabels)
  (GROUP_CONCAT(DISTINCT ?locationId;   separator="|") AS ?locationIds)
  (GROUP_CONCAT(DISTINCT ?locationLabel;separator="|") AS ?locationLabels)
  (GROUP_CONCAT(DISTINCT ?coordStr;     separator="|") AS ?coordStrs)
WHERE {{
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "en".
  }}

  {type_filter}
  ?item wdt:P31 ?itemType.

  OPTIONAL {{ ?item wdt:P580 ?startTimeIndicator. }}
  OPTIONAL {{ ?item wdt:P585 ?pointInTime. }}
  BIND(IF(BOUND(?startTimeIndicator), ?startTimeIndicator, ?pointInTime) AS ?startTime)

  OPTIONAL {{ ?item wdt:P582 ?endTime. }}

  OPTIONAL {{
    ?item schema:description ?description.
    FILTER(LANG(?description) = "en")
  }}

  OPTIONAL {{ ?item wdt:P18 ?imageUrl. }}

  OPTIONAL {{
    ?article schema:about ?item ;
             schema:isPartOf <https://en.wikipedia.org/> ;
             schema:name ?wpTitle .
    BIND(
      IRI(CONCAT("https://en.wikipedia.org/wiki/", ENCODE_FOR_URI(?wpTitle)))
      AS ?wikipediaUrl
    )
  }}

  OPTIONAL {{
    ?item wdt:P17 ?countryEntity.
    ?countryEntity rdfs:label ?countryLabel.
    FILTER(LANG(?countryLabel) = "en")
    BIND(REPLACE(STR(?countryEntity), "http://www.wikidata.org/entity/", "") AS ?countryId)
  }}

  OPTIONAL {{
    ?item wdt:P276 ?locationEntity.
    ?locationEntity rdfs:label ?locationLabel.
    FILTER(LANG(?locationLabel) = "en")
    BIND(REPLACE(STR(?locationEntity), "http://www.wikidata.org/entity/", "") AS ?locationId)
    OPTIONAL {{
      ?locationEntity wdt:P625 ?coord.
      BIND(CONCAT(STR(geof:latitude(?coord)), ",", STR(geof:longitude(?coord))) AS ?coordStr)
    }}
  }}

  {location_filter}

  FILTER(?startTime >= "{timeslot_start}"^^xsd:dateTime)
  FILTER(?startTime <= "{timeslot_end}"^^xsd:dateTime)
}}
GROUP BY ?item ?itemLabel ?itemType ?startTime ?endTime ?description ?imageUrl ?wikipediaUrl
ORDER BY DESC(?startTime)
LIMIT {page_size}
OFFSET {offset}
"""

_COUNT_QUERY_TEMPLATE = """
SELECT (COUNT(DISTINCT ?item) AS ?total)
WHERE {{
  {type_filter}
  ?item wdt:P31 ?itemType.

  OPTIONAL {{ ?item wdt:P580 ?startTimeIndicator. }}
  OPTIONAL {{ ?item wdt:P585 ?pointInTime. }}
  BIND(IF(BOUND(?startTimeIndicator), ?startTimeIndicator, ?pointInTime) AS ?startTime)

  {location_filter}

  FILTER(?startTime >= "{timeslot_start}"^^xsd:dateTime)
  FILTER(?startTime <= "{timeslot_end}"^^xsd:dateTime)
}}
"""


def _default_date_range() -> tuple[str, str]:
    now = datetime.now(UTC)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    return (
        (now - timedelta(days=30)).strftime(fmt),
        (now + timedelta(days=30)).strftime(fmt),
    )


def _build_location_filter(filters: dict) -> str:
    regions = filters.get("regions") or []
    countries = filters.get("countries") or []

    region_qcodes = get_country_qcodes_for_regions(regions) if regions else []
    country_iso_codes = []
    if countries:
        for iso in countries:
            if not re.match(r"^[A-Z]{3}$", iso):
                raise ValueError(f"Invalid ISO 3166-1 alpha-3 country code: '{iso}'")
            country_iso_codes.append(iso)

    if region_qcodes and country_iso_codes:
        wd_values = " ".join(f"wd:{q}" for q in region_qcodes)
        iso_values = " ".join(f'"{c}"' for c in country_iso_codes)
        return f"""{{
  VALUES ?regionCountry {{ {wd_values} }}
  ?item wdt:P17 ?regionCountry.
}} UNION {{
  VALUES ?iso3Code {{ {iso_values} }}
  ?isoCountry wdt:P298 ?iso3Code.
  ?item wdt:P17 ?isoCountry.
}}"""
    elif region_qcodes:
        wd_values = " ".join(f"wd:{q}" for q in region_qcodes)
        return f"""VALUES ?regionCountry {{ {wd_values} }}
  ?item wdt:P17 ?regionCountry."""
    elif country_iso_codes:
        iso_values = " ".join(f'"{c}"' for c in country_iso_codes)
        return f"""VALUES ?iso3Code {{ {iso_values} }}
  ?isoCountry wdt:P298 ?iso3Code.
  ?item wdt:P17 ?isoCountry."""
    return ""


def _sparql_query(query: str) -> dict:
    sparql = SPARQLWrapper(SPARQL_ENDPOINT, agent=SPARQL_USER_AGENT)
    sparql.setTimeout(SPARQL_TIMEOUT_SECONDS)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    logger.debug("Executing SPARQL query: %s", query)
    try:
        results = sparql.query().convert()
    except Exception as exc:
        logger.error("SPARQL query failed: %s", exc)
        raise
    return cast(dict, results)


def count_events_v2(filters: dict) -> int:
    timeslot_start, timeslot_end = _default_date_range()
    if filters.get("timeslot_start"):
        timeslot_start = filters["timeslot_start"]
    if filters.get("timeslot_end"):
        timeslot_end = filters["timeslot_end"]

    type_filter = WikidataClassEnum.to_sparql_values_block(filters.get("types"))
    location_filter = _build_location_filter(filters)

    query = _COUNT_QUERY_TEMPLATE.format(
        type_filter=type_filter,
        location_filter=location_filter,
        timeslot_start=timeslot_start,
        timeslot_end=timeslot_end,
    )

    results = _sparql_query(query)
    bindings = results["results"]["bindings"]
    if bindings:
        return int(bindings[0]["total"]["value"])
    return 0


def get_event_dao_list_v2(filters: dict, page: int, page_size: int) -> list[dict]:
    timeslot_start, timeslot_end = _default_date_range()
    if filters.get("timeslot_start"):
        timeslot_start = filters["timeslot_start"]
    if filters.get("timeslot_end"):
        timeslot_end = filters["timeslot_end"]

    type_filter = WikidataClassEnum.to_sparql_values_block(filters.get("types"))
    location_filter = _build_location_filter(filters)
    offset = (page - 1) * page_size

    query = _MAIN_QUERY_TEMPLATE.format(
        type_filter=type_filter,
        location_filter=location_filter,
        timeslot_start=timeslot_start,
        timeslot_end=timeslot_end,
        page_size=page_size,
        offset=offset,
    )

    results = _sparql_query(query)
    return results["results"]["bindings"]
