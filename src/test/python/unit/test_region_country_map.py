import unittest

from event_resolver.persistence.models.region_country_map import (
    REGION_COUNTRY_QCODES,
    get_country_qcodes_for_regions,
)

ALL_REGIONS = [
    "EUROPE_AND_CENTRAL_ASIA",
    "MIDDLE_EAST_AND_NORTH_AFRICA",
    "NORTH_AMERICA",
    "EAST_ASIA_AND_PACIFIC",
    "SOUTH_ASIA",
    "LATIN_AMERICA_AND_CARIBBEAN",
    "SUB_SAHARAN_AFRICA",
]


class TestRegionCountryMap(unittest.TestCase):
    def test_all_seven_regions_present(self):
        self.assertEqual(set(REGION_COUNTRY_QCODES.keys()), set(ALL_REGIONS))

    def test_north_america_contains_usa(self):
        self.assertIn("Q30", get_country_qcodes_for_regions(["NORTH_AMERICA"]))

    def test_europe_contains_germany_and_france(self):
        codes = get_country_qcodes_for_regions(["EUROPE_AND_CENTRAL_ASIA"])
        self.assertIn("Q183", codes)  # Germany
        self.assertIn("Q142", codes)  # France

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(get_country_qcodes_for_regions([]), [])

    def test_unknown_region_returns_empty_list(self):
        self.assertEqual(get_country_qcodes_for_regions(["NONEXISTENT_REGION"]), [])

    def test_multiple_regions_are_combined(self):
        codes = get_country_qcodes_for_regions(["NORTH_AMERICA", "SOUTH_ASIA"])
        self.assertIn("Q30", codes)  # USA (NORTH_AMERICA)
        self.assertIn("Q668", codes)  # India (SOUTH_ASIA)

    def test_no_duplicates_when_regions_overlap(self):
        codes = get_country_qcodes_for_regions(["NORTH_AMERICA", "NORTH_AMERICA"])
        self.assertEqual(len(codes), len(set(codes)))

    def test_all_qcodes_are_q_format(self):
        for region, codes in REGION_COUNTRY_QCODES.items():
            for code in codes:
                self.assertTrue(
                    code.startswith("Q") and code[1:].isdigit(),
                    f"Invalid Q-code '{code}' in region '{region}'",
                )

    def test_no_qcode_appears_in_multiple_regions(self):
        from collections import Counter

        all_pairs = []
        for region, codes in REGION_COUNTRY_QCODES.items():
            all_pairs.extend((code, region) for code in codes)
        counts = Counter(code for code, _ in all_pairs)
        duplicates = {code: [r for c, r in all_pairs if c == code] for code, n in counts.items() if n > 1}
        self.assertEqual(
            duplicates,
            {},
            f"Q-codes appear in multiple regions (cross-region contamination): {duplicates}",
        )
