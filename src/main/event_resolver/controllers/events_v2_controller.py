from event_resolver.service import events_v2_service


def v2_events_get(
    page: int = 1,
    page_size: int = 100,
    types: list[str] | None = None,
    regions: list[str] | None = None,
    countries: list[str] | None = None,
    timeslot_start: str | None = None,
    timeslot_end: str | None = None,
):
    result = events_v2_service.get_events_v2(
        page=page,
        page_size=page_size,
        types=types,
        regions=regions,
        countries=countries,
        timeslot_start=timeslot_start,
        timeslot_end=timeslot_end,
    )
    return result.to_dict()
