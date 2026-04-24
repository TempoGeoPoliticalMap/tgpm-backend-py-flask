from unittest.mock import patch

from python.test_events import BaseTestCase


class TestMetadataController(BaseTestCase):

    def test_event_types_returns_200(self):
        response = self.client.get(
            "/v2/metadata/event-types",
            headers={"Accept": "application/json"},
        )
        self.assert200(response)

    def test_event_types_returns_ten_items(self):
        body = self.client.get("/v2/metadata/event-types").json()
        self.assertEqual(len(body["data"]), 10)

    def test_event_types_items_have_required_fields(self):
        body = self.client.get("/v2/metadata/event-types").json()
        for item in body["data"]:
            self.assertIn("code", item)
            self.assertIn("name", item)
            self.assertIn("description", item)

    def test_regions_returns_200(self):
        response = self.client.get(
            "/v2/metadata/regions",
            headers={"Accept": "application/json"},
        )
        self.assert200(response)

    def test_regions_returns_seven_items(self):
        body = self.client.get("/v2/metadata/regions").json()
        self.assertEqual(len(body["data"]), 7)

    @patch("event_resolver.service.metadata_service.count_country_codes", return_value=10)
    @patch(
        "event_resolver.service.metadata_service.get_country_codes_dao",
        return_value=[{"code": "GBR", "name": "United Kingdom"}],
    )
    def test_country_codes_returns_200(self, mock_dao, mock_count):
        response = self.client.get(
            "/v2/metadata/country-codes",
            headers={"Accept": "application/json"},
        )
        self.assert200(response)

    @patch("event_resolver.service.metadata_service.count_country_codes", return_value=10)
    @patch(
        "event_resolver.service.metadata_service.get_country_codes_dao",
        return_value=[{"code": "GBR", "name": "United Kingdom"}],
    )
    def test_country_codes_response_has_data_and_pagination(self, mock_dao, mock_count):
        body = self.client.get("/v2/metadata/country-codes").json()
        self.assertIn("data", body)
        self.assertIn("pagination", body)

    @patch("event_resolver.service.metadata_service.count_country_codes", return_value=2)
    @patch(
        "event_resolver.service.metadata_service.get_country_codes_dao",
        return_value=[{"code": "GBR", "name": "United Kingdom"}],
    )
    def test_country_codes_search_query_accepted(self, mock_dao, mock_count):
        response = self.client.get(
            "/v2/metadata/country-codes?q=united",
            headers={"Accept": "application/json"},
        )
        self.assert200(response)
