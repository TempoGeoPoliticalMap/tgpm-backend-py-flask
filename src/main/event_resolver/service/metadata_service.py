import math

from event_resolver.persistence.repository.metadata_storage import (
    count_country_codes,
    get_country_codes_dao,
)
from openapi_models.models.pagination import Pagination

MAX_PAGE_SIZE = 100

EVENT_TYPE_METADATA = [
    {
        "code": "GEOPOLITICAL_GROUP",
        "name": "Geopolitical Group",
        "description": "Political grouping of states with shared geopolitical interests.",
    },
    {
        "code": "INTERNATIONAL_ORGANISATION",
        "name": "International Organisation",
        "description": "Intergovernmental organisation operating across multiple countries.",
    },
    {
        "code": "MILITARY_ALLIANCE",
        "name": "Military Alliance",
        "description": "Formal military alliance between states.",
    },
    {
        "code": "MULTINATIONAL_MILITARY_COALITION",
        "name": "Multinational Military Coalition",
        "description": "Coalition of multiple countries formed for military operations.",
    },
    {
        "code": "POLITICAL_CONFERENCE",
        "name": "Political Conference",
        "description": "Formal political conference involving state or institutional actors.",
    },
    {
        "code": "POLITICAL_CRISIS",
        "name": "Political Crisis",
        "description": "Significant political instability or confrontation.",
    },
    {
        "code": "POLITICAL_MURDER",
        "name": "Political Murder",
        "description": "Politically motivated assassination or killing.",
    },
    {
        "code": "SOURCE_OF_INTERNATIONAL_LAW",
        "name": "Source of International Law",
        "description": "Treaty, convention, or other recognised source of international law.",
    },
    {
        "code": "SUPRANATIONAL_UNION",
        "name": "Supranational Union",
        "description": "Union in which member states delegate authority to shared institutions.",
    },
    {
        "code": "WARFARE_AND_ARMED_CONFLICTS",
        "name": "Warfare and Armed Conflicts",
        "description": "Armed hostilities, military operations, and violent conflict between organised actors.",
    },
]

REGION_METADATA = [
    {
        "code": "EAST_ASIA_AND_PACIFIC",
        "name": "East Asia and Pacific",
        "description": "Countries in East Asia, Southeast Asia, and Pacific island regions.",
    },
    {
        "code": "EUROPE_AND_CENTRAL_ASIA",
        "name": "Europe and Central Asia",
        "description": "Countries in Europe and Central Asia.",
    },
    {
        "code": "LATIN_AMERICA_AND_CARIBBEAN",
        "name": "Latin America and Caribbean",
        "description": "Countries in Latin America and Caribbean regions.",
    },
    {
        "code": "MIDDLE_EAST_AND_NORTH_AFRICA",
        "name": "Middle East and North Africa",
        "description": "Countries in the Middle East and North Africa.",
    },
    {
        "code": "NORTH_AMERICA",
        "name": "North America",
        "description": "Countries in North America.",
    },
    {
        "code": "SOUTH_ASIA",
        "name": "South Asia",
        "description": "Countries in South Asia.",
    },
    {
        "code": "SUB_SAHARAN_AFRICA",
        "name": "Sub-Saharan Africa",
        "description": "Countries in Sub-Saharan Africa.",
    },
]


def get_event_types() -> list[dict]:
    return EVENT_TYPE_METADATA


def get_regions() -> list[dict]:
    return REGION_METADATA


def get_country_codes(page: int, page_size: int, q: str | None) -> dict:
    page = max(page, 1)
    page_size = min(max(page_size, 1), MAX_PAGE_SIZE)

    total_items = count_country_codes(q)
    total_pages = math.ceil(total_items / page_size) if page_size > 0 else 0
    items = get_country_codes_dao(page, page_size, q)

    pagination = Pagination(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next_page=page < total_pages,
    )
    return {"data": items, "pagination": pagination.to_dict()}
