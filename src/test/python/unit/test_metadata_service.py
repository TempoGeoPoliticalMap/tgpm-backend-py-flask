import unittest
from unittest.mock import patch

from event_resolver.service import metadata_service


class TestMetadataService(unittest.TestCase):
    def test_get_event_types_returns_ten_items(self):
        result = metadata_service.get_event_types()
        self.assertEqual(len(result), 10)

    def test_get_event_types_all_have_required_fields(self):
        for item in metadata_service.get_event_types():
            self.assertIn("code", item)
            self.assertIn("name", item)
            self.assertIn("description", item)
            self.assertTrue(item["code"].isupper())

    def test_get_regions_returns_seven_items(self):
        result = metadata_service.get_regions()
        self.assertEqual(len(result), 7)

    def test_get_regions_all_have_required_fields(self):
        for item in metadata_service.get_regions():
            self.assertIn("code", item)
            self.assertIn("name", item)
            self.assertIn("description", item)

    def test_event_type_codes_match_spec_enum(self):
        expected = {
            "GEOPOLITICAL_GROUP",
            "INTERNATIONAL_ORGANISATION",
            "MILITARY_ALLIANCE",
            "MULTINATIONAL_MILITARY_COALITION",
            "POLITICAL_CONFERENCE",
            "POLITICAL_CRISIS",
            "POLITICAL_MURDER",
            "SOURCE_OF_INTERNATIONAL_LAW",
            "SUPRANATIONAL_UNION",
            "WARFARE_AND_ARMED_CONFLICTS",
        }
        actual = {item["code"] for item in metadata_service.get_event_types()}
        self.assertEqual(actual, expected)

    def test_region_codes_match_spec_enum(self):
        expected = {
            "EAST_ASIA_AND_PACIFIC",
            "EUROPE_AND_CENTRAL_ASIA",
            "LATIN_AMERICA_AND_CARIBBEAN",
            "MIDDLE_EAST_AND_NORTH_AFRICA",
            "NORTH_AMERICA",
            "SOUTH_ASIA",
            "SUB_SAHARAN_AFRICA",
        }
        actual = {item["code"] for item in metadata_service.get_regions()}
        self.assertEqual(actual, expected)

    @patch("event_resolver.service.metadata_service.count_country_codes", return_value=30)
    @patch(
        "event_resolver.service.metadata_service.get_country_codes_dao",
        return_value=[{"code": "GBR", "name": "United Kingdom"}],
    )
    def test_get_country_codes_returns_pagination(self, mock_dao, mock_count):
        result = metadata_service.get_country_codes(page=1, page_size=10, q=None)
        self.assertIn("data", result)
        self.assertIn("pagination", result)
        pagination = result["pagination"]
        self.assertEqual(pagination.get("total_items") or pagination.get("totalItems"), 30)
        self.assertEqual(pagination.get("total_pages") or pagination.get("totalPages"), 3)
        self.assertTrue(pagination.get("has_next_page") or pagination.get("hasNextPage"))

    @patch("event_resolver.service.metadata_service.count_country_codes", return_value=0)
    @patch("event_resolver.service.metadata_service.get_country_codes_dao", return_value=[])
    def test_get_country_codes_empty_result(self, mock_dao, mock_count):
        result = metadata_service.get_country_codes(page=1, page_size=10, q=None)
        self.assertEqual(result["data"], [])
        pagination = result["pagination"]
        self.assertFalse(pagination.get("has_next_page") or pagination.get("hasNextPage"))

    @patch("event_resolver.service.metadata_service.count_country_codes", return_value=5)
    @patch("event_resolver.service.metadata_service.get_country_codes_dao", return_value=[])
    def test_search_query_forwarded_to_storage(self, mock_dao, mock_count):
        metadata_service.get_country_codes(page=1, page_size=100, q="united")
        mock_count.assert_called_once_with("united")
        mock_dao.assert_called_once_with(1, 100, "united")
