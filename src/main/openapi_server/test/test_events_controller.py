# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

import openapi_server
from openapi_server.models.error400 import Error400  # noqa: E501
from openapi_server.models.error403 import Error403  # noqa: E501
from openapi_server.models.event_list_response_body import EventListResponseBody  # noqa: E501
from openapi_server.models.event_type import EventType  # noqa: E501
from openapi_server.models.region import Region  # noqa: E501
from openapi_server.test import BaseTestCase


class TestEventsController(BaseTestCase):
    """EventsController integration test stubs"""

    def test_v1_events_get(self):
        """Test case for v1_events_get

        List of Historical Political Events.
        """
        query_string = [('types', ['elections,war']),
                        ('regions', ['east_asia_and_pacific,middle_east_and_north_africa']),
                        ('countries', ['fra,gbr']),
                        ('timeslot_start', '2013-10-20T19:20:30+01:00'),
                        ('timeslot_end', '2022-05-30T18:20:00Z')]
        headers = {
            'Accept': 'application/json',
            'accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/events',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
