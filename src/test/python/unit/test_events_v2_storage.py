from unittest.mock import patch

from event_resolver.persistence.repository.events_v2_storage import (
    count_events_v2,
    get_event_dao_list_v2,
)

_FILTERS = {
    "types": ["WARFARE_AND_ARMED_CONFLICTS"],
    "regions": ["EUROPE_AND_CENTRAL_ASIA"],
    "countries": None,
    "timeslot_start": "2022-01-01T00:00:00Z",
    "timeslot_end": "2022-03-30T18:20:00Z",
}


class TestEventsV2Storage:
    @patch("event_resolver.persistence.repository.events_v2_storage._sparql_query")
    def test_count_query_filters_by_direct_p31(self, mock_sparql):
        mock_sparql.return_value = {"results": {"bindings": [{"total": {"value": "0"}}]}}

        count_events_v2(_FILTERS)

        query = mock_sparql.call_args[0][0]
        assert "VALUES ?rootType" in query
        assert "wdt:P31 ?rootType" in query
        assert "wdt:P31/wdt:P279*" not in query
        assert "wd:Q71266556" in query
        assert "wd:Q198" in query
        assert "wd:Q467011" in query

    @patch("event_resolver.persistence.repository.events_v2_storage._sparql_query")
    def test_main_query_filters_by_direct_p31(self, mock_sparql):
        mock_sparql.return_value = {"results": {"bindings": []}}

        get_event_dao_list_v2(filters=_FILTERS, page=1, page_size=10)

        query = mock_sparql.call_args[0][0]
        assert "VALUES ?rootType" in query
        assert "wdt:P31 ?rootType" in query
        assert "wdt:P31/wdt:P279*" not in query
        assert "MIN(?rootType)" in query
        assert "LIMIT 10" in query
        assert "OFFSET 0" in query

    @patch("event_resolver.persistence.repository.events_v2_storage._sparql_query")
    def test_main_query_offset_advances_with_page(self, mock_sparql):
        mock_sparql.return_value = {"results": {"bindings": []}}

        get_event_dao_list_v2(filters=_FILTERS, page=3, page_size=10)

        query = mock_sparql.call_args[0][0]
        assert "OFFSET 20" in query
