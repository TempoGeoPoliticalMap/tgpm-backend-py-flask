import unittest

from event_resolver.persistence.models.wikidata_class_enum import WikidataClassEnum

V2_API_EVENT_TYPES = [
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
]


class TestWikidataClassEnum(unittest.TestCase):

    def test_all_ten_v2_event_types_are_mapped(self):
        block = WikidataClassEnum.to_sparql_values_block(V2_API_EVENT_TYPES)
        self.assertIsInstance(block, str)
        self.assertIn("VALUES ?itemType", block)

    def test_sparql_block_contains_all_qcodes_when_no_filter(self):
        block = WikidataClassEnum.to_sparql_values_block(None)
        self.assertIn("wd:Q71266556", block)  # WARFARE_AND_ARMED_CONFLICTS
        self.assertIn("wd:Q1139665", block)   # POLITICAL_MURDER
        self.assertIn("wd:Q52110228", block)  # GEOPOLITICAL_GROUP

    def test_sparql_block_is_filtered_when_types_provided(self):
        block = WikidataClassEnum.to_sparql_values_block(["POLITICAL_MURDER"])
        self.assertIn("wd:Q1139665", block)
        self.assertNotIn("wd:Q71266556", block)  # WARFARE should be excluded

    def test_sparql_block_contains_all_qcodes_when_empty_list(self):
        block = WikidataClassEnum.to_sparql_values_block([])
        self.assertIn("wd:Q71266556", block)

    def test_qcodes_are_valid_format(self):
        for member in WikidataClassEnum:
            raw = member.value.replace("wd:", "")
            self.assertTrue(
                raw.startswith("Q") and raw[1:].isdigit(),
                f"Invalid Q-code format for {member.name}: {member.value}",
            )
