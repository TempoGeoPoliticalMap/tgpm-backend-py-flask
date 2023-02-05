# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

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
from openapi_server.test import BaseTestCase


class TestEventsController(BaseTestCase):
    """EventsController integration test stubs"""

    def test_v1_events_get(self):
        """Test case for v1_events_get

        List of Historical Political Events.
        """
        headers = {
            "Accept": "application/json",
            "accept": "application/json",
        }
        response = self.client.open("/v1/events", method="GET", headers=headers)
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
