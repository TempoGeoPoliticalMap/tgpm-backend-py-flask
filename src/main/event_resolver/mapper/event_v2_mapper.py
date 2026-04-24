from datetime import UTC, datetime

from event_resolver.persistence.models.region_country_map import REGION_COUNTRY_QCODES
from openapi_models.models.country import Country
from openapi_models.models.event_event import EventEvent
from openapi_models.models.location import Location

_WIKIDATA_ENTITY_PREFIX = "http://www.wikidata.org/entity/"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# Reverse lookup: Q-code → API event-type string
_QCODE_TO_API_TYPE: dict[str, str] = {
    "Q52110228": "GEOPOLITICAL_GROUP",
    "Q484652": "INTERNATIONAL_ORGANISATION",
    "Q1127126": "MILITARY_ALLIANCE",
    "Q100906234": "MULTINATIONAL_MILITARY_COALITION",
    "Q17195514": "POLITICAL_CONFERENCE",
    "Q3002772": "POLITICAL_CRISIS",
    "Q1139665": "POLITICAL_MURDER",
    "Q2635077": "SOURCE_OF_INTERNATIONAL_LAW",
    "Q1335818": "SUPRANATIONAL_UNION",
    "Q71266556": "WARFARE_AND_ARMED_CONFLICTS",
}

# Reverse lookup: Q-code → region name
_QCODE_TO_REGION: dict[str, str] = {
    qcode: region
    for region, qcodes in REGION_COUNTRY_QCODES.items()
    for qcode in qcodes
}


def _extract_qcode(uri: str) -> str:
    return uri.replace(_WIKIDATA_ENTITY_PREFIX, "")


def _resolve_time_state(start_dt_str: str, end_dt_str: str | None) -> str:
    now = datetime.now(UTC)
    start_dt = datetime.strptime(start_dt_str, _DATE_FORMAT).replace(
        tzinfo=UTC
    )
    if start_dt > now:
        return "FUTURE"
    if end_dt_str is not None:
        end_dt = datetime.strptime(end_dt_str, _DATE_FORMAT).replace(
            tzinfo=UTC
        )
        if end_dt <= now:
            return "PAST"
    return "ONGOING"


def map_binding(binding: dict) -> EventEvent:
    """Map a SPARQL binding dict to an EventEvent model instance."""
    item_uri = binding["item"]["value"]
    wikidata_id = _extract_qcode(item_uri)
    wikidata_url = f"https://www.wikidata.org/wiki/{wikidata_id}"

    item_type_uri = binding["itemType"]["value"]
    item_type_qcode = _extract_qcode(item_type_uri)
    event_type = _QCODE_TO_API_TYPE.get(item_type_qcode, item_type_qcode)

    start_dt_str = binding["startTime"]["value"]
    end_dt_str = binding.get("endTime", {}).get("value")

    time_state = _resolve_time_state(start_dt_str, end_dt_str)

    country_ids = binding.get("countryIds", {}).get("value", "").split("|")
    country_labels = binding.get("countryLabels", {}).get("value", "").split("|")
    countries = [
        Country(wikidata_id=i, name=n)
        for i, n in zip(country_ids, country_labels)
        if i
    ]

    location_ids = binding.get("locationIds", {}).get("value", "").split("|")
    location_labels = binding.get("locationLabels", {}).get("value", "").split("|")
    coord_strs = binding.get("coordStrs", {}).get("value", "").split("|")
    locations = [
        Location(wikidata_id=i, name=n, coordinate=c)
        for i, n, c in zip(location_ids, location_labels, coord_strs)
        if i and c
    ]

    region_set: list[str] = list(
        dict.fromkeys(
            _QCODE_TO_REGION[i] for i in country_ids if i and i in _QCODE_TO_REGION
        )
    )

    return EventEvent(
        type=event_type,
        wikidata_id=wikidata_id,
        wikidata_url=wikidata_url,
        name=binding["itemLabel"]["value"],
        description=binding.get("description", {}).get("value"),
        wikipedia_url=binding.get("wikipediaUrl", {}).get("value"),
        image_url=binding.get("imageUrl", {}).get("value"),
        regions=region_set,
        countries=countries,
        locations=locations,
        time_state_relative_to_now=time_state,
        start_date_time=start_dt_str,
        end_date_time=end_dt_str,
    )
