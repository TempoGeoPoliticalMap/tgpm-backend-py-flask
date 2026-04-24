import unittest
from unittest.mock import patch

from python.test_events import BaseTestCase


class TestEventsController(BaseTestCase):
    """EventsController integration test stubs"""

    def test_v1_events_get(self):
        """Test case for v1_events_get"""
        with patch(
            "event_resolver.service.events_service.get_event_dao_list",
            return_value={"bindings": []},
        ):
            response = self.client.get("/v1/events", headers={"Accept": "application/json"})
        self.assert200(response, "Response body is : " + response.text)


if __name__ == "__main__":
    unittest.main()
