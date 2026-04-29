import unittest
from unittest.mock import MagicMock, patch

from event_resolver.persistence.repository.events_v2_storage import UpstreamTimeoutError
from event_resolver.service import events_v2_service

_BLANK_NODE = "http://www.wikidata.org/.well-known/genid/f9702a193120719c02b44e41e81717c0"

_VALID_BINDING = {
    "item": {"value": "http://www.wikidata.org/entity/Q138503695"},
    "itemLabel": {"value": "2026 Iran war"},
    "itemType": {"value": "http://www.wikidata.org/entity/Q71266556"},
    "startTime": {"value": "2026-02-28T00:00:00Z"},
    "countryIds": {"value": "Q794"},
    "countryLabels": {"value": "Iran"},
    "locationIds": {"value": ""},
    "locationLabels": {"value": ""},
    "coordStrs": {"value": ""},
}

_BINDING_WITH_BLANK_NODE_END_TIME = {**_VALID_BINDING, "endTime": {"value": _BLANK_NODE}}
_BINDING_WITH_BLANK_NODE_START_TIME = {**_VALID_BINDING, "startTime": {"value": _BLANK_NODE}}


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
        self.assertEqual(call_filters["types"], ["POLITICAL_MURDER"])
        self.assertEqual(call_filters["regions"], ["NORTH_AMERICA"])
        self.assertEqual(call_filters["countries"], ["USA"])
        self.assertEqual(call_filters["timeslot_start"], "2024-01-01T00:00:00Z")
        self.assertEqual(call_filters["timeslot_end"], "2024-12-31T23:59:59Z")

    @patch("event_resolver.service.events_v2_service.count_events_v2", return_value=1)
    @patch(
        "event_resolver.service.events_v2_service.get_event_dao_list_v2",
        return_value=[_BINDING_WITH_BLANK_NODE_END_TIME],
    )
    def test_binding_with_blank_node_end_time_is_included(self, mock_list, mock_count):
        result = events_v2_service.get_events_v2()
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].name, "2026 Iran war")
        self.assertIsNone(result.data[0].end_date_time)

    @patch("event_resolver.service.events_v2_service.count_events_v2", return_value=1)
    @patch(
        "event_resolver.service.events_v2_service.get_event_dao_list_v2",
        return_value=[_BINDING_WITH_BLANK_NODE_START_TIME],
    )
    def test_binding_with_blank_node_start_time_is_excluded(self, mock_list, mock_count):
        result = events_v2_service.get_events_v2()
        self.assertEqual(len(result.data), 0)

    @patch(
        "event_resolver.service.events_v2_service.count_events_v2",
        side_effect=UpstreamTimeoutError("The read operation timed out"),
    )
    @patch("event_resolver.service.events_v2_service.get_event_dao_list_v2")
    def test_count_timeout_uses_page_size_plus_one_fallback(self, mock_list, mock_count):
        mock_list.return_value = [_VALID_BINDING] * 11

        result = events_v2_service.get_events_v2(page=1, page_size=10)

        self.assertEqual(len(result.data), 10)
        self.assertTrue(result.pagination.has_next_page)
        self.assertEqual(result.pagination.total_items, 11)
        self.assertEqual(result.pagination.total_pages, 2)
        mock_list.assert_called_once()
        args = mock_list.call_args[0]
        self.assertEqual(args[1], 1)
        self.assertEqual(args[2], 11)

    @patch(
        "event_resolver.service.events_v2_service.count_events_v2",
        side_effect=UpstreamTimeoutError("The read operation timed out"),
    )
    @patch("event_resolver.service.events_v2_service.get_event_dao_list_v2")
    def test_count_timeout_without_extra_items_has_no_next_page(self, mock_list, mock_count):
        mock_list.return_value = [_VALID_BINDING] * 3

        result = events_v2_service.get_events_v2(page=1, page_size=10)

        self.assertEqual(len(result.data), 3)
        self.assertFalse(result.pagination.has_next_page)
        self.assertEqual(result.pagination.total_items, 3)
        self.assertEqual(result.pagination.total_pages, 1)
