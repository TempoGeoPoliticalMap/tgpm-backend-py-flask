import events_service
from openapi_server.models.event_list_response_body import (
    EventListResponseBody,
)  # noqa: E501


def v1_events_get(accept=None):  # noqa: E501
    """List of Historical Political Events.

     # noqa: E501

    :param accept: Default accept header
    :type accept: str

    :rtype: EventListResponseBody
    """
    result = events_service.get_events()

    for r in result:
        print(r)

    return result
