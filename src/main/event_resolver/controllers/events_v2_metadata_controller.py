from event_resolver.service import metadata_service


def v2_metadata_event_types_get():
    return {"data": metadata_service.get_event_types()}


def v2_metadata_regions_get():
    return {"data": metadata_service.get_regions()}


def v2_metadata_country_codes_get(
    page: int = 1,
    page_size: int = 100,
    q: str | None = None,
):
    return metadata_service.get_country_codes(page=page, page_size=page_size, q=q)
