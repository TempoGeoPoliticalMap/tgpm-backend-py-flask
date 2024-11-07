from event_resolver.service import events_service
from openapi_models.models.event_list_response_body import (
    EventListResponseBody,
)  # noqa: E501


def v1_events_get():  # noqa: E501
    """List of Historical Political Events.

     # noqa: E501

    :param accept: Default accept header
    :type accept: str

    :rtype: EventListResponseBody
    """
    result = events_service.get_events()

    return [event.to_dict() for event in result]
