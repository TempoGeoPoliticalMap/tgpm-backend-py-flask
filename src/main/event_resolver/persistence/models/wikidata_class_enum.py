import enum


class WikidataClassEnum(enum.Enum):
    GEOPOLITICAL_GROUP = "wd:Q52110228"  # https://www.wikidata.org/wiki/Q52110228
    INTERNATION_ORGANIZATION = "wd:Q484652"  # https://www.wikidata.org/wiki/Q484652
    MILITARY_ALLIANCE = "wd:Q1127126"  # https://www.wikidata.org/wiki/Q1127126
    MULTINATIONAL_MILITARY_COALITION = (
        "wd:Q100906234"  # https://www.wikidata.org/wiki/Q100906234
    )
    POLITICAL_CONFERENCE = "wd:Q17195514"  # https://www.wikidata.org/wiki/Q17195514
    POLITICAL_CRISIS = "wd:Q3002772"  # https://www.wikidata.org/wiki/Q3002772
    POLITICAL_MURDER = "wd:Q1139665"  # https://www.wikidata.org/wiki/Q1139665
    SOURCES_OF_INTERNATIONAL_LAW = (
        "wd:Q2635077"  # https://www.wikidata.org/wiki/Q2635077
    )
    SUPRANATIONAL_UNION = "wd:Q1335818"  # https://www.wikidata.org/wiki/Q1335818
    WARFARE_AND_ARMED_CONFLICTS = (
        "wd:Q71266556"  # https://www.wikidata.org/wiki/Q71266556
    )

    @staticmethod
    def to_sparql_values_block(selected_types: list[str] | None) -> str:
        if not selected_types:
            members = list(WikidataClassEnum)
        else:
            members = []
            for api_val in selected_types:
                member = API_TO_WIKIDATA_ENUM.get(api_val)
                if member is None:
                    raise ValueError(f"Unknown event type API value: '{api_val}'")
                members.append(member)
        qcodes = " ".join(m.value for m in members)
        return f"VALUES ?itemType {{ {qcodes} }}"


# Maps v2 API event-type strings to WikidataClassEnum members.
# Two members diverge from their API counterparts:
#   INTERNATION_ORGANIZATION  (enum typo) == INTERNATIONAL_ORGANISATION (API / spec)
#   SOURCES_OF_INTERNATIONAL_LAW (plural) == SOURCE_OF_INTERNATIONAL_LAW (API / spec)
# Never resolve by enum member name directly — always go through this dict.
API_TO_WIKIDATA_ENUM: dict[str, WikidataClassEnum] = {
    "GEOPOLITICAL_GROUP": WikidataClassEnum.GEOPOLITICAL_GROUP,
    "INTERNATIONAL_ORGANISATION": WikidataClassEnum.INTERNATION_ORGANIZATION,
    "MILITARY_ALLIANCE": WikidataClassEnum.MILITARY_ALLIANCE,
    "MULTINATIONAL_MILITARY_COALITION": WikidataClassEnum.MULTINATIONAL_MILITARY_COALITION,
    "POLITICAL_CONFERENCE": WikidataClassEnum.POLITICAL_CONFERENCE,
    "POLITICAL_CRISIS": WikidataClassEnum.POLITICAL_CRISIS,
    "POLITICAL_MURDER": WikidataClassEnum.POLITICAL_MURDER,
    "SOURCE_OF_INTERNATIONAL_LAW": WikidataClassEnum.SOURCES_OF_INTERNATIONAL_LAW,
    "SUPRANATIONAL_UNION": WikidataClassEnum.SUPRANATIONAL_UNION,
    "WARFARE_AND_ARMED_CONFLICTS": WikidataClassEnum.WARFARE_AND_ARMED_CONFLICTS,
}
