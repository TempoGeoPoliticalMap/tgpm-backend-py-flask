# Wikidata Mappings

## Event type Q-code table

**Source:** `src/main/event_resolver/persistence/models/wikidata_class_enum.py`

The API accepts event type values (e.g. `WARFARE_AND_ARMED_CONFLICTS`) which are
translated to Wikidata Q-codes via `API_TO_WIKIDATA_ENUM`. Two names diverge between
the enum member and the API string — both cases are handled by the translation dict.
Never resolve by enum member name directly.

| API value (`types` query param) | Enum member | Wikidata Q-code | Wikidata link |
|---|---|---|---|
| `GEOPOLITICAL_GROUP` | `GEOPOLITICAL_GROUP` | Q52110228 | https://www.wikidata.org/wiki/Q52110228 |
| `INTERNATIONAL_ORGANISATION` | `INTERNATION_ORGANIZATION` *(typo — do not fix)* | Q484652 | https://www.wikidata.org/wiki/Q484652 |
| `MILITARY_ALLIANCE` | `MILITARY_ALLIANCE` | Q1127126 | https://www.wikidata.org/wiki/Q1127126 |
| `MULTINATIONAL_MILITARY_COALITION` | `MULTINATIONAL_MILITARY_COALITION` | Q100906234 | https://www.wikidata.org/wiki/Q100906234 |
| `POLITICAL_CONFERENCE` | `POLITICAL_CONFERENCE` | Q17195514 | https://www.wikidata.org/wiki/Q17195514 |
| `POLITICAL_CRISIS` | `POLITICAL_CRISIS` | Q3002772 | https://www.wikidata.org/wiki/Q3002772 |
| `POLITICAL_MURDER` | `POLITICAL_MURDER` | Q1139665 | https://www.wikidata.org/wiki/Q1139665 |
| `SOURCE_OF_INTERNATIONAL_LAW` | `SOURCES_OF_INTERNATIONAL_LAW` *(plural — do not fix)* | Q2635077 | https://www.wikidata.org/wiki/Q2635077 |
| `SUPRANATIONAL_UNION` | `SUPRANATIONAL_UNION` | Q1335818 | https://www.wikidata.org/wiki/Q1335818 |
| `WARFARE_AND_ARMED_CONFLICTS` | `WARFARE_AND_ARMED_CONFLICTS` | Q71266556 | https://www.wikidata.org/wiki/Q71266556 |

> **Note:** `INTERNATION_ORGANIZATION` and `SOURCES_OF_INTERNATIONAL_LAW` are intentional
> preserved typos in the enum. Renaming them would break v1 code. The `API_TO_WIKIDATA_ENUM`
> dict is the single place that bridges the mismatch.

---

## Region → country Q-code table

**Source:** `src/main/event_resolver/persistence/models/region_country_map.py`

Used to expand `regions` filter values into Wikidata country Q-codes for SPARQL injection.

### EUROPE_AND_CENTRAL_ASIA (50 countries)

| Q-code | Country |
|---|---|
| Q183 | Germany |
| Q142 | France |
| Q145 | United Kingdom |
| Q38 | Italy |
| Q29 | Spain |
| Q212 | Ukraine |
| Q159 | Russia |
| Q36 | Poland |
| Q55 | Netherlands |
| Q31 | Belgium |
| Q39 | Switzerland |
| Q40 | Austria |
| Q34 | Sweden |
| Q20 | Norway |
| Q35 | Denmark |
| Q33 | Finland |
| Q213 | Czech Republic |
| Q28 | Hungary |
| Q218 | Romania |
| Q219 | Bulgaria |
| Q41 | Greece |
| Q45 | Portugal |
| Q43 | Turkey |
| Q232 | Kazakhstan |
| Q265 | Uzbekistan |
| Q230 | Georgia |
| Q399 | Armenia |
| Q227 | Azerbaijan |
| Q184 | Belarus |
| Q403 | Serbia |
| Q224 | Croatia |
| Q225 | Bosnia and Herzegovina |
| Q217 | Moldova |
| Q222 | Albania |
| Q221 | North Macedonia |
| Q236 | Montenegro |
| Q1246 | Kosovo |
| Q215 | Slovenia |
| Q211 | Latvia |
| Q37 | Lithuania |
| Q191 | Estonia |
| Q229 | Cyprus |
| Q233 | Malta |
| Q32 | Luxembourg |
| Q27 | Ireland |
| Q189 | Iceland |
| Q214 | Slovakia |
| Q863 | Tajikistan |
| Q813 | Kyrgyzstan |
| Q880 | Turkmenistan |

### MIDDLE_EAST_AND_NORTH_AFRICA

| Q-code | Country |
|---|---|
| Q858 | Syria |
| Q796 | Iraq |
| Q794 | Iran |
| Q851 | Saudi Arabia |
| Q801 | Israel |
| Q219060 | Palestine |
| Q783 | Jordan |
| Q805 | Yemen |
| Q811 | Oman |
| Q817 | Kuwait |
| Q816 | Bahrain |
| Q846 | Qatar |
| Q878 | United Arab Emirates |
| Q781 | Lebanon |
| Q262 | Algeria |
| Q948 | Tunisia |
| Q1016 | Libya |
| Q1049 | Sudan |
| Q79 | Egypt |
| Q1028 | Morocco |
| Q1025 | Mauritania |

### NORTH_AMERICA

| Q-code | Country |
|---|---|
| Q30 | United States |
| Q16 | Canada |
| Q96 | Mexico |

### EAST_ASIA_AND_PACIFIC

See `region_country_map.py` for the full list of ~32 countries including China (Q29520),
Japan (Q17), South Korea (Q884), Australia (Q408), and Pacific island nations.

### SOUTH_ASIA

| Q-code | Country |
|---|---|
| Q668 | India |
| Q843 | Pakistan |
| Q902 | Bangladesh |
| Q837 | Nepal |
| Q854 | Sri Lanka |
| Q889 | Afghanistan |
| Q826 | Maldives |
| Q917 | Bhutan |

### LATIN_AMERICA_AND_CARIBBEAN

See `region_country_map.py` for the full list of ~31 countries including Brazil (Q155),
Argentina (Q414), Colombia (Q739), and Caribbean island nations.

### SUB_SAHARAN_AFRICA

See `region_country_map.py` for the full list of ~48 countries including Nigeria (Q1033),
Ethiopia (Q115), South Africa (Q258), and Kenya (Q114).

---

## Invariant enforced by tests

`test_no_qcode_appears_in_multiple_regions` in `unit/test_region_country_map.py` verifies
that no Q-code appears in more than one region. This prevents double-counting when the
SPARQL `VALUES` block is built.
