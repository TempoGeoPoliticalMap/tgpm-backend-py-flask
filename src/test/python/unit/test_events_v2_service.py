import unittest
from unittest.mock import MagicMock, patch

from event_resolver.service import events_v2_service


class TestEventsV2Service(unittest.TestCase):

    def _make_mock_event(self):
        e = MagicMock()
        e.to_dict.return_value = {"type": "POLITICAL_MURDER", "name": "Test"}
        return e

    @patch("event_resolver.service.events_v2_service.count_events_v2", return_value=25)
    @patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=[{}] * 10)
    @patch("event_resolver.service.events_v2_service.map_binding")
    def test_pagination_metadata_is_correct(self, mock_map, mock_list, mock_count):
        mock_map.return_value = self._make_mock_event()
        result = events_v2_service.get_events_v2(page=2, page_size=10)
        p = result.pagination
        self.assertEqual(p.page, 2)
        self.assertEqual(p.page_size, 10)
        self.assertEqual(p.total_items, 25)
        self.assertEqual(p.total_pages, 3)
        self.assertTrue(p.has_next_page)

    @patch("event_resolver.service.events_v2_service.count_events_v2", return_value=0)
    @patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=[])
    @patch("event_resolver.service.events_v2_service.map_binding")
    def test_empty_result_returns_valid_response(self, mock_map, mock_list, mock_count):
        result = events_v2_service.get_events_v2()
        self.assertEqual(result.data, [])
        self.assertEqual(result.pagination.total_items, 0)
        self.assertFalse(result.pagination.has_next_page)

    @patch("event_resolver.service.events_v2_service.count_events_v2", return_value=5)
    @patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=[{}] * 5)
    @patch("event_resolver.service.events_v2_service.map_binding")
    def test_last_page_has_no_next_page(self, mock_map, mock_list, mock_count):
        mock_map.return_value = self._make_mock_event()
        result = events_v2_service.get_events_v2(page=1, page_size=10)
        self.assertFalse(result.pagination.has_next_page)

    @patch("event_resolver.service.events_v2_service.count_events_v2", return_value=10)
    @patch("event_resolver.service.events_v2_service.get_event_dao_list_v2")
    @patch("event_resolver.service.events_v2_service.map_binding")
    def test_filters_are_forwarded_to_storage(self, mock_map, mock_list, mock_count):
        mock_list.return_value = []
        mock_map.return_value = self._make_mock_event()
        events_v2_service.get_events_v2(
            types=["POLITICAL_MURDER"],
            regions=["NORTH_AMERICA"],
            countries=["USA"],
            timeslot_start="2024-01-01T00:00:00Z",
            timeslot_end="2024-12-31T23:59:59Z",
        )
        call_filters = mock_list.call_args[0][0]
        self.assertEqual(call_filters["types"],           ["POLITICAL_MURDER"])
        self.assertEqual(call_filters["regions"],         ["NORTH_AMERICA"])
        self.assertEqual(call_filters["countries"],       ["USA"])
        self.assertEqual(call_filters["timeslot_start"],  "2024-01-01T00:00:00Z")
        self.assertEqual(call_filters["timeslot_end"],    "2024-12-31T23:59:59Z")
