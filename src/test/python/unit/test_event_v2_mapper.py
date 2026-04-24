import unittest

from event_resolver.mapper import event_v2_mapper

_BLANK_NODE = "http://www.wikidata.org/.well-known/genid/f9702a193120719c02b44e41e81717c0"

FULL_BINDING = {
    "item": {"value": "http://www.wikidata.org/entity/Q178810"},
    "itemLabel": {"value": "Syrian Civil War"},
    "itemType": {"value": "http://www.wikidata.org/entity/Q71266556"},
    "startTime": {"value": "2011-03-15T00:00:00Z"},
    "endTime": {"value": "2025-01-01T00:00:00Z"},
    "description": {"value": "An ongoing civil war in Syria."},
    "imageUrl": {"value": "https://upload.wikimedia.org/example.jpg"},
    "wikipediaUrl": {"value": "https://en.wikipedia.org/wiki/Syrian_civil_war"},
    "countryIds": {"value": "Q858|Q796"},
    "countryLabels": {"value": "Syria|Iraq"},
    "locationIds": {"value": "Q858"},
    "locationLabels": {"value": "Syria"},
    "coordStrs": {"value": "33.51,36.29"},
}

MINIMAL_BINDING = {
    "item": {"value": "http://www.wikidata.org/entity/Q178810"},
    "itemLabel": {"value": "Syrian Civil War"},
    "itemType": {"value": "http://www.wikidata.org/entity/Q71266556"},
    "startTime": {"value": "2011-03-15T00:00:00Z"},
    "countryIds": {"value": ""},
    "countryLabels": {"value": ""},
    "locationIds": {"value": ""},
    "locationLabels": {"value": ""},
    "coordStrs": {"value": ""},
}


class TestEventV2Mapper(unittest.TestCase):
    def test_required_fields_populated(self):
        event = event_v2_mapper.map_binding(FULL_BINDING)
        self.assertEqual(event.wikidata_id, "Q178810")
        self.assertEqual(event.wikidata_url, "https://www.wikidata.org/wiki/Q178810")
        self.assertEqual(event.name, "Syrian Civil War")
        self.assertEqual(event.type, "WARFARE_AND_ARMED_CONFLICTS")
        self.assertEqual(event.start_date_time, "2011-03-15T00:00:00Z")

    def test_optional_fields_populated_when_present(self):
        event = event_v2_mapper.map_binding(FULL_BINDING)
        self.assertEqual(event.description, "An ongoing civil war in Syria.")
        self.assertEqual(event.image_url, "https://upload.wikimedia.org/example.jpg")
        self.assertEqual(event.wikipedia_url, "https://en.wikipedia.org/wiki/Syrian_civil_war")
        self.assertEqual(event.end_date_time, "2025-01-01T00:00:00Z")

    def test_countries_parsed(self):
        event = event_v2_mapper.map_binding(FULL_BINDING)
        self.assertEqual(len(event.countries), 2)
        self.assertEqual(event.countries[0].wikidata_id, "Q858")
        self.assertEqual(event.countries[0].name, "Syria")

    def test_locations_parsed(self):
        event = event_v2_mapper.map_binding(FULL_BINDING)
        self.assertEqual(len(event.locations), 1)
        self.assertEqual(event.locations[0].wikidata_id, "Q858")
        self.assertEqual(event.locations[0].coordinate, "33.51,36.29")

    def test_regions_derived_from_countries(self):
        event = event_v2_mapper.map_binding(FULL_BINDING)
        self.assertIn("MIDDLE_EAST_AND_NORTH_AFRICA", event.regions)

    def test_empty_countries_and_locations_when_absent(self):
        event = event_v2_mapper.map_binding(MINIMAL_BINDING)
        self.assertEqual(event.countries, [])
        self.assertEqual(event.locations, [])
        self.assertEqual(event.regions, [])

    def test_optional_fields_are_none_when_absent(self):
        event = event_v2_mapper.map_binding(MINIMAL_BINDING)
        self.assertIsNone(event.description)
        self.assertIsNone(event.image_url)
        self.assertIsNone(event.wikipedia_url)
        self.assertIsNone(event.end_date_time)

    def test_time_state_future(self):
        binding = dict(MINIMAL_BINDING)
        binding["startTime"] = {"value": "2099-01-01T00:00:00Z"}
        event = event_v2_mapper.map_binding(binding)
        self.assertEqual(event.time_state_relative_to_now, "FUTURE")

    def test_time_state_past(self):
        binding = dict(FULL_BINDING)
        binding["startTime"] = {"value": "2000-01-01T00:00:00Z"}
        binding["endTime"] = {"value": "2001-01-01T00:00:00Z"}
        event = event_v2_mapper.map_binding(binding)
        self.assertEqual(event.time_state_relative_to_now, "PAST")

    def test_time_state_ongoing(self):
        binding = dict(MINIMAL_BINDING)
        binding["startTime"] = {"value": "2000-01-01T00:00:00Z"}
        event = event_v2_mapper.map_binding(binding)
        self.assertEqual(event.time_state_relative_to_now, "ONGOING")

    def test_wikidata_url_format(self):
        event = event_v2_mapper.map_binding(MINIMAL_BINDING)
        self.assertTrue(event.wikidata_url.startswith("https://www.wikidata.org/wiki/Q"))

    def test_blank_node_end_time_is_treated_as_none(self):
        binding = dict(MINIMAL_BINDING)
        binding["startTime"] = {"value": "2026-02-28T00:00:00Z"}
        binding["endTime"] = {"value": _BLANK_NODE}
        event = event_v2_mapper.map_binding(binding)
        self.assertIsNone(event.end_date_time)

    def test_blank_node_end_time_yields_ongoing_state(self):
        binding = dict(MINIMAL_BINDING)
        binding["startTime"] = {"value": "2026-02-28T00:00:00Z"}
        binding["endTime"] = {"value": _BLANK_NODE}
        event = event_v2_mapper.map_binding(binding)
        self.assertEqual(event.time_state_relative_to_now, "ONGOING")


class TestIsValidBinding(unittest.TestCase):
    def test_valid_binding_with_end_time(self):
        self.assertTrue(event_v2_mapper.is_valid_binding(FULL_BINDING))

    def test_valid_binding_without_end_time(self):
        self.assertTrue(event_v2_mapper.is_valid_binding(MINIMAL_BINDING))

    def test_blank_node_start_time_is_invalid(self):
        binding = dict(MINIMAL_BINDING)
        binding["startTime"] = {"value": _BLANK_NODE}
        self.assertFalse(event_v2_mapper.is_valid_binding(binding))

    def test_blank_node_end_time_is_valid(self):
        binding = dict(MINIMAL_BINDING)
        binding["endTime"] = {"value": _BLANK_NODE}
        self.assertTrue(event_v2_mapper.is_valid_binding(binding))

    def test_missing_start_time_is_invalid(self):
        binding = {k: v for k, v in MINIMAL_BINDING.items() if k != "startTime"}
        self.assertFalse(event_v2_mapper.is_valid_binding(binding))
