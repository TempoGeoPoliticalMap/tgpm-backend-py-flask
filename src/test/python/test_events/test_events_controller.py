# coding: utf-8

from __future__ import absolute_import
import unittest

from python.test_events import BaseTestCase


class TestEventsController(BaseTestCase):
    """EventsController integration test_events stubs"""

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
