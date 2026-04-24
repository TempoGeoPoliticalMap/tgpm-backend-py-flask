import math

from event_resolver.mapper.event_v2_mapper import map_binding
from event_resolver.persistence.repository.events_v2_storage import (
    count_events_v2,
    get_event_dao_list_v2,
)
from openapi_models.models.event_event_list_response_body import (
    EventEventListResponseBody,
)
from openapi_models.models.pagination import Pagination

MAX_PAGE_SIZE = 100


def get_events_v2(
    page: int = 1,
    page_size: int = 100,
    types: list[str] | None = None,
    regions: list[str] | None = None,
    countries: list[str] | None = None,
    timeslot_start: str | None = None,
    timeslot_end: str | None = None,
) -> EventEventListResponseBody:
    page = max(page, 1)
    page_size = min(max(page_size, 1), MAX_PAGE_SIZE)

    filters = {
        "types": types,
        "regions": regions,
        "countries": countries,
        "timeslot_start": timeslot_start,
        "timeslot_end": timeslot_end,
    }

    total_items = count_events_v2(filters)
    total_pages = math.ceil(total_items / page_size) if page_size > 0 else 0
    has_next_page = page < total_pages

    bindings = get_event_dao_list_v2(filters, page, page_size)
    events = [map_binding(b) for b in bindings]

    pagination = Pagination(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next_page=has_next_page,
    )

    return EventEventListResponseBody(data=events, pagination=pagination)
