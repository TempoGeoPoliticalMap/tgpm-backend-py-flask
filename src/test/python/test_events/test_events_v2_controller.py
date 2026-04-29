from unittest.mock import patch

from python.test_events import BaseTestCase

from event_resolver.persistence.repository.exceptions import (
    UpstreamRateLimitError,
    UpstreamUnavailableError,
)


class TestEventsV2Controller(BaseTestCase):
    def _make_bindings(self, count=2):
        return [
            {
                "item": {"value": "http://www.wikidata.org/entity/Q1"},
                "itemLabel": {"value": "Test Event"},
                "itemType": {"value": "http://www.wikidata.org/entity/Q71266556"},
                "startTime": {"value": "2024-06-01T00:00:00Z"},
                "countryIds": {"value": ""},
                "countryLabels": {"value": ""},
                "locationIds": {"value": ""},
                "locationLabels": {"value": ""},
                "coordStrs": {"value": ""},
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
            patch(
                "event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=self._make_bindings(5)
            ),
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
                "/v2/events?timeslot_start=2024-01-01T00:00:00Z&timeslot_end=2024-12-31T23:59:59Z",
                headers={"Accept": "application/json"},
            )
        self.assert200(response)

    def test_v2_events_returns_429_when_upstream_rate_limited(self):
        with patch(
            "event_resolver.service.events_v2_service.count_events_v2",
            side_effect=UpstreamRateLimitError("Upstream data source rate limited", retry_after="60"),
        ):
            response = self.client.get("/v2/events", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.headers.get("Retry-After"), "60")
        self.assertIn("rate limited", response.json()["detail"])

    def test_v2_events_returns_502_when_upstream_disconnects(self):
        with patch(
            "event_resolver.service.events_v2_service.count_events_v2",
            side_effect=UpstreamUnavailableError("Upstream data source unavailable"),
        ):
            response = self.client.get("/v2/events", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 502)
        self.assertIn("unavailable", response.json()["detail"])

    def test_v2_events_empty_types_param_treated_as_omitted(self):
        """?types= (key present, empty value) must not cause a 400."""
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=0),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=[]),
        ):
            response = self.client.get("/v2/events?types=")
        self.assert200(response)

    def test_v2_events_empty_regions_param_treated_as_omitted(self):
        """?regions= (key present, empty value) must not cause a 400."""
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=0),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=[]),
        ):
            response = self.client.get("/v2/events?regions=")
        self.assert200(response)

    def test_v2_events_empty_types_and_regions_treated_as_omitted(self):
        """?types=&regions= together must not cause a 400."""
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=0),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=[]),
        ):
            response = self.client.get("/v2/events?types=&regions=")
        self.assert200(response)

    def test_iran_war_with_blank_node_end_time_is_returned(self):
        """2026 Iran war has a Wikidata blank-node endTime; it must still appear in the response."""
        iran_war_binding = {
            "item": {"value": "http://www.wikidata.org/entity/Q138503695"},
            "itemLabel": {"value": "2026 Iran war"},
            "itemType": {"value": "http://www.wikidata.org/entity/Q71266556"},
            "startTime": {"value": "2026-02-28T00:00:00Z"},
            "endTime": {"value": "http://www.wikidata.org/.well-known/genid/f9702a193120719c02b44e41e81717c0"},
            "countryIds": {"value": "Q794"},
            "countryLabels": {"value": "Iran"},
            "locationIds": {"value": ""},
            "locationLabels": {"value": ""},
            "coordStrs": {"value": ""},
        }
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=1),
            patch("event_resolver.service.events_v2_service.get_event_dao_list_v2", return_value=[iran_war_binding]),
        ):
            body = self.client.get(
                "/v2/events?page=1&pageSize=10"
                "&types=WARFARE_AND_ARMED_CONFLICTS"
                "&regions=MIDDLE_EAST_AND_NORTH_AFRICA"
                "&timeslot_start=2022-01-01T00:00:00Z"
                "&timeslot_end=2026-03-30T18:20:00Z"
            ).json()
        self.assertEqual(len(body["data"]), 1)
        event = body["data"][0]
        self.assertEqual(event["name"], "2026 Iran war")
        self.assertIsNone(event["endDateTime"])

    def test_2022_ukrainian_war_is_returned_for_requested_query(self):
        ukrainian_war_binding = {
            "item": {"value": "http://www.wikidata.org/entity/Q110999040"},
            "itemLabel": {"value": "2022 Ukrainian war"},
            "itemType": {"value": "http://www.wikidata.org/entity/Q71266556"},
            "startTime": {"value": "2022-02-24T00:00:00Z"},
            "countryIds": {"value": "Q212|Q159"},
            "countryLabels": {"value": "Ukraine|Russia"},
            "locationIds": {"value": ""},
            "locationLabels": {"value": ""},
            "coordStrs": {"value": ""},
        }
        with (
            patch("event_resolver.service.events_v2_service.count_events_v2", return_value=1),
            patch(
                "event_resolver.service.events_v2_service.get_event_dao_list_v2",
                return_value=[ukrainian_war_binding],
            ),
        ):
            body = self.client.get(
                "/v2/events?page=1&pageSize=10"
                "&types=WARFARE_AND_ARMED_CONFLICTS"
                "&regions=EUROPE_AND_CENTRAL_ASIA"
                "&timeslot_start=2022-01-01T00:00:00Z"
                "&timeslot_end=2022-03-30T18:20:00Z"
            ).json()
        self.assertEqual(len(body["data"]), 1)
        self.assertEqual(body["data"][0]["name"], "2022 Ukrainian war")

    def test_v1_events_still_works(self):
        """Backward compatibility guard: v1 must not be broken."""
        with patch(
            "event_resolver.service.events_service.get_event_dao_list",
            return_value={"bindings": []},
        ):
            response = self.client.get("/v1/events", headers={"Accept": "application/json"})
        self.assert200(response)
