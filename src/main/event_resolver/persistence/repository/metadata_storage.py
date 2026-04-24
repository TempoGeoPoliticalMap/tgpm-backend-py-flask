import logging
import re
from typing import cast

from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
SPARQL_USER_AGENT = (
    "TGPM-Backend/1.0 (https://github.com/TempoGeoPoliticalMap; contact@tgpm.org)"
)
SPARQL_TIMEOUT_SECONDS = 30

_COUNTRY_CODES_QUERY = """
SELECT DISTINCT ?iso3 ?countryLabel WHERE {{
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
  ?country wdt:P31 wd:Q6256.
  ?country wdt:P298 ?iso3.
  {search_filter}
}}
ORDER BY ASC(?iso3)
LIMIT {page_size}
OFFSET {offset}
"""

_COUNTRY_CODES_COUNT_QUERY = """
SELECT (COUNT(DISTINCT ?country) AS ?total) WHERE {{
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
  ?country wdt:P31 wd:Q6256.
  ?country wdt:P298 ?iso3.
  {search_filter}
}}
"""


def _sanitize_search_term(q: str) -> str:
    if not re.match(r"^[\w\s\-]+$", q, re.UNICODE):
        raise ValueError(f"Invalid search term: '{q}'")
    return q.replace('"', "").replace("\\", "")


def _build_search_filter(q: str | None) -> str:
    if not q:
        return ""
    sanitized = _sanitize_search_term(q)
    return (
        f'FILTER(\n'
        f'  CONTAINS(LCASE(STR(?countryLabel)), LCASE("{sanitized}")) ||\n'
        f'  CONTAINS(LCASE(?iso3), LCASE("{sanitized}"))\n'
        f")"
    )


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


def count_country_codes(q: str | None) -> int:
    search_filter = _build_search_filter(q)
    query = _COUNTRY_CODES_COUNT_QUERY.format(search_filter=search_filter)
    results = _sparql_query(query)
    bindings = results["results"]["bindings"]
    if bindings:
        return int(bindings[0]["total"]["value"])
    return 0


def get_country_codes_dao(page: int, page_size: int, q: str | None) -> list[dict]:
    search_filter = _build_search_filter(q)
    offset = (page - 1) * page_size
    query = _COUNTRY_CODES_QUERY.format(
        search_filter=search_filter,
        page_size=page_size,
        offset=offset,
    )
    results = _sparql_query(query)
    return [
        {
            "code": b["iso3"]["value"],
            "name": b.get("countryLabel", {}).get("value", b["iso3"]["value"]),
        }
        for b in results["results"]["bindings"]
    ]
