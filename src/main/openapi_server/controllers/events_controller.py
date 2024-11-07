import connexion
import six

from openapi_server.service import events_service
from openapi_server.models.basic_error_object import BasicErrorObject  # noqa: E501
from openapi_server.models.error400 import Error400  # noqa: E501
from openapi_server.models.error401 import Error401  # noqa: E501
from openapi_server.models.error403 import Error403  # noqa: E501
from openapi_server.models.error404 import Error404  # noqa: E501
from openapi_server.models.error406 import Error406  # noqa: E501
from openapi_server.models.error429 import Error429  # noqa: E501
from openapi_server.models.event_list_response_body import (
    EventListResponseBody,
)  # noqa: E501
from openapi_server import util


def v1_events_get(accept=None):  # noqa: E501
    """List of Historical Political Events.

     # noqa: E501

    :param accept: Default accept header
    :type accept: str

    :rtype: EventListResponseBody
    """
    result = events_service.get_events()

    return result
