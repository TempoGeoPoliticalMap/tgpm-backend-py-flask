import connexion
import six

from openapi_server.models.error400 import Error400  # noqa: E501
from openapi_server.models.error403 import Error403  # noqa: E501
from openapi_server.models.event_list_response_body import EventListResponseBody  # noqa: E501
from openapi_server.models.event_type import EventType  # noqa: E501
from openapi_server.models.region import Region  # noqa: E501
from openapi_server import util


def v1_events_get(accept=None, types=None, regions=None, countries=None, timeslot_start=None,
                  timeslot_end=None):  # noqa: E501
    """List of Historical Political Events.

     # noqa: E501

    :param accept: Default accept header
    :type accept: str
    :param types: Type(s) of an Event:&lt;br&gt; &lt;ul&gt; &lt;li&gt;&#x60;elections&#x60; - State elections, e.g. presidential, parliament etc.&lt;/li&gt; &lt;li&gt;&#x60;war&#x60; - Wars or military conflicts.&lt;/li&gt; &lt;/ul&gt;
    :type types: list | bytes
    :param regions: World Regions.&lt;br&gt; &lt;ul&gt; &lt;li&gt;&#x60;east_asia_and_pacific&#x60;&lt;/li&gt; &lt;li&gt;&#x60;europe_and_central_asia&#x60;&lt;/li&gt; &lt;li&gt;&#x60;latin_america_and_caribbean&#x60;&lt;/li&gt; &lt;li&gt;&#x60;middle_east_and_north_africa&#x60;&lt;/li&gt; &lt;li&gt;&#x60;north_america&#x60;&lt;/li&gt; &lt;li&gt;&#x60;south_asia&#x60;&lt;/li&gt; &lt;li&gt;&#x60;sub_saharan_africa&#x60;&lt;/li&gt; &lt;/ul&gt;
    :type regions: list | bytes
    :param countries: Country code(s) to filter Events by.
    :type countries: List[str]
    :param timeslot_start: Timeslot Start Date/Time to filter by.
    :type timeslot_start: str
    :param timeslot_end: Timeslot End Date/Time to filter by.
    :type timeslot_end: str

    :rtype: EventListResponseBody
    """
    if connexion.request.is_json:
        types = [EventType.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    if connexion.request.is_json:
        regions = [Region.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    timeslot_start = util.deserialize_datetime(timeslot_start)
    timeslot_end = util.deserialize_datetime(timeslot_end)
    return 'do some magic!'
