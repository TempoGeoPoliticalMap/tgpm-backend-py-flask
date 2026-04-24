from unittest.mock import patch

from python.test_events import BaseTestCase


class TestEventsV2Controller(BaseTestCase):

    def _make_bindings(self, count=2):
        return [
            {
                "item":           {"value": "http://www.wikidata.org/entity/Q1"},
                "itemLabel":      {"value": "Test Event"},
                "itemType":       {"value": "http://www.wikidata.org/entity/Q71266556"},
                "startTime":      {"value": "2024-06-01T00:00:00Z"},
                "countryIds":     {"value": ""},
                "countryLabels":  {"value": ""},
                "locationIds":    {"value": ""},
                "locationLabels": {"value": ""},
                "coordStrs":      {"value": ""},
            }
        ] * count

    def test_v2_events_get_returns_200(self):
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=2),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=self._make_bindings()),
        ):
            response = self.client.get("/v2/events", headers={"Accept": "application/json"})
        self.assert200(response)

    def test_v2_events_response_has_data_and_pagination(self):
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=2),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=self._make_bindings()),
        ):
            body = self.client.get("/v2/events").json()
        self.assertIn("data", body)
        self.assertIn("pagination", body)
        for key in ("page", "pageSize", "totalItems", "totalPages", "hasNextPage"):
            self.assertIn(key, body["pagination"])

    def test_v2_events_pagination_values_are_correct(self):
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=5),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=self._make_bindings(5)),
        ):
            body = self.client.get("/v2/events?page=1&pageSize=10").json()
        self.assertEqual(body["pagination"]["page"], 1)
        self.assertEqual(body["pagination"]["pageSize"], 10)
        self.assertEqual(body["pagination"]["totalItems"], 5)

    def test_v2_events_with_type_filter(self):
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=2),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=self._make_bindings()),
        ):
            response = self.client.get(
                "/v2/events?types=WARFARE_AND_ARMED_CONFLICTS",
                headers={"Accept": "application/json"},
            )
        self.assert200(response)

    def test_v2_events_with_region_filter(self):
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=2),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=self._make_bindings()),
        ):
            response = self.client.get(
                "/v2/events?regions=EUROPE_AND_CENTRAL_ASIA",
                headers={"Accept": "application/json"},
            )
        self.assert200(response)

    def test_v2_events_with_country_filter(self):
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=2),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=self._make_bindings()),
        ):
            response = self.client.get(
                "/v2/events?countries=GBR,FRA",
                headers={"Accept": "application/json"},
            )
        self.assert200(response)

    def test_v2_events_with_date_filters(self):
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=2),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=self._make_bindings()),
        ):
            response = self.client.get(
                "/v2/events?timeslot_start=2024-01-01T00:00:00Z"
                "&timeslot_end=2024-12-31T23:59:59Z",
                headers={"Accept": "application/json"},
            )
        self.assert200(response)

    def test_v1_events_still_works(self):
        """Backward compatibility guard: v1 must not be broken."""
        with patch(
            "event_resolver.service.events_service.get_event_dao_list",
            return_value={"bindings": []},
        ):
            response = self.client.get(
                "/v1/events", headers={"Accept": "application/json"}
            )
        self.assert200(response)
