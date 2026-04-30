import unittest

from python.test_events import BaseTestCase


class TestCors(BaseTestCase):

    def test_get_request_has_allow_origin_header(self):
        """Regular GET responses must carry Access-Control-Allow-Origin."""
        response = self.client.get(
            "/v2/metadata/event-types",
            headers={"Origin": "https://app.example.com"},
        )
        self.assert200(response)
        self.assertIn("Access-Control-Allow-Origin", response.headers)

    def test_options_preflight_returns_200(self):
        """Browser preflight (OPTIONS) must be answered before routing."""
        response = self.client.options(
            "/v2/events",
            headers={
                "Origin": "https://app.example.com",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        self.assertIn(response.status_code, (200, 204))

    def test_options_preflight_has_allow_origin_header(self):
        """Preflight response must include Access-Control-Allow-Origin."""
        response = self.client.options(
            "/v2/events",
            headers={
                "Origin": "https://app.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        self.assertIn("Access-Control-Allow-Origin", response.headers)
