import unittest
from unittest.mock import patch

from event_resolver.persistence.repository.metadata_storage import (
    _build_search_filter,
    count_country_codes,
    get_country_codes_dao,
)

_EMPTY_COUNT = {"results": {"bindings": [{"total": {"value": "0"}}]}}
_EMPTY_LIST = {"results": {"bindings": []}}


class TestBuildSearchFilter(unittest.TestCase):

    def test_empty_when_no_query(self):
        self.assertEqual(_build_search_filter(None), "")
        self.assertEqual(_build_search_filter(""), "")

    def test_contains_country_label_variable(self):
        result = _build_search_filter("uni")
        self.assertIn("?countryLabel", result)

    def test_contains_iso3_variable(self):
        result = _build_search_filter("gbr")
        self.assertIn("?iso3", result)

    def test_search_term_present_in_filter(self):
        result = _build_search_filter("united")
        self.assertIn("united", result)

    def test_invalid_term_raises(self):
        with self.assertRaises(ValueError):
            _build_search_filter("'; DROP TABLE--")


class TestCountryCodesQueryContainsRdfsLabel(unittest.TestCase):
    """Verify the generated SPARQL binds ?countryLabel via rdfs:label so
    FILTER(CONTAINS(...?countryLabel...)) actually works at query time."""

    @patch("event_resolver.persistence.repository.metadata_storage._sparql_query")
    def test_get_dao_query_uses_rdfs_label(self, mock_sparql):
        mock_sparql.return_value = _EMPTY_LIST
        get_country_codes_dao(page=1, page_size=10, q="uni")
        query = mock_sparql.call_args[0][0]
        self.assertIn("rdfs:label", query)

    @patch("event_resolver.persistence.repository.metadata_storage._sparql_query")
    def test_get_dao_query_includes_search_term(self, mock_sparql):
        mock_sparql.return_value = _EMPTY_LIST
        get_country_codes_dao(page=1, page_size=10, q="uni")
        query = mock_sparql.call_args[0][0]
        self.assertIn("uni", query)

    @patch("event_resolver.persistence.repository.metadata_storage._sparql_query")
    def test_count_query_uses_rdfs_label(self, mock_sparql):
        mock_sparql.return_value = _EMPTY_COUNT
        count_country_codes("uni")
        query = mock_sparql.call_args[0][0]
        self.assertIn("rdfs:label", query)

    @patch("event_resolver.persistence.repository.metadata_storage._sparql_query")
    def test_count_query_includes_search_term(self, mock_sparql):
        mock_sparql.return_value = _EMPTY_COUNT
        count_country_codes("uni")
        query = mock_sparql.call_args[0][0]
        self.assertIn("uni", query)

    @patch("event_resolver.persistence.repository.metadata_storage._sparql_query")
    def test_no_search_filter_still_uses_rdfs_label(self, mock_sparql):
        mock_sparql.return_value = _EMPTY_LIST
        get_country_codes_dao(page=1, page_size=10, q=None)
        query = mock_sparql.call_args[0][0]
        self.assertIn("rdfs:label", query)
