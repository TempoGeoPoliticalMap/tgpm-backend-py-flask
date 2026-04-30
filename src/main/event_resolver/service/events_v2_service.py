import logging
import math

from event_resolver.mapper.event_v2_mapper import is_valid_binding, map_binding
from event_resolver.persistence.repository.events_v2_storage import (
    UpstreamTimeoutError,
    count_events_v2,
    get_event_dao_list_v2,
)
from openapi_models.models.event_list_response_body import (
    EventListResponseBody,
)
from openapi_models.models.pagination import Pagination

MAX_PAGE_SIZE = 100
logger = logging.getLogger(__name__)


def get_events_v2(
    page: int = 1,
    page_size: int = 25,
    types: list[str] | None = None,
    regions: list[str] | None = None,
    countries: list[str] | None = None,
    timeslot_start: str | None = None,
    timeslot_end: str | None = None,
) -> EventListResponseBody:
    page = max(page, 1)
    page_size = min(max(page_size, 1), MAX_PAGE_SIZE)

    filters = {
        "types": types,
        "regions": regions,
        "countries": countries,
        "timeslot_start": timeslot_start,
        "timeslot_end": timeslot_end,
    }

    try:
        total_items = count_events_v2(filters)
        total_pages = math.ceil(total_items / page_size) if page_size > 0 else 0
        has_next_page = page < total_pages
        bindings = get_event_dao_list_v2(filters, page, page_size)
    except UpstreamTimeoutError:
        logger.warning(
            "count_events_v2 timed out for page=%s page_size=%s; using pagination fallback",
            page,
            page_size,
        )
        fallback_bindings = get_event_dao_list_v2(filters, page, page_size + 1)
        has_next_page = len(fallback_bindings) > page_size
        bindings = fallback_bindings[:page_size]
        total_items = (page - 1) * page_size + len(bindings) + (1 if has_next_page else 0)
        total_pages = page + 1 if has_next_page else page

    events = [map_binding(b) for b in bindings if is_valid_binding(b)]

    pagination = Pagination(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next_page=has_next_page,
    )

    return EventListResponseBody(data=events, pagination=pagination)
