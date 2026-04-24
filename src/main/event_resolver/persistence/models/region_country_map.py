REGION_COUNTRY_QCODES: dict[str, list[str]] = {
    "EUROPE_AND_CENTRAL_ASIA": [
        "Q183",  # Germany
        "Q142",  # France
        "Q145",  # United Kingdom
        "Q38",  # Italy
        "Q29",  # Spain
        "Q212",  # Ukraine
        "Q159",  # Russia
        "Q36",  # Poland
        "Q55",  # Netherlands
        "Q31",  # Belgium
        "Q39",  # Switzerland
        "Q40",  # Austria
        "Q34",  # Sweden
        "Q20",  # Norway
        "Q35",  # Denmark
        "Q33",  # Finland
        "Q213",  # Czech Republic
        "Q28",  # Hungary
        "Q218",  # Romania
        "Q219",  # Bulgaria
        "Q41",  # Greece
        "Q45",  # Portugal
        "Q43",  # Turkey
        "Q232",  # Kazakhstan
        "Q265",  # Uzbekistan
        "Q230",  # Georgia
        "Q399",  # Armenia
        "Q227",  # Azerbaijan
        "Q184",  # Belarus
        "Q403",  # Serbia
        "Q224",  # Croatia
        "Q225",  # Bosnia and Herzegovina
        "Q217",  # Moldova
        "Q222",  # Albania
        "Q221",  # North Macedonia
        "Q236",  # Montenegro
        "Q1246",  # Kosovo
        "Q215",  # Slovenia
        "Q211",  # Latvia
        "Q37",  # Lithuania
        "Q191",  # Estonia
        "Q229",  # Cyprus
        "Q233",  # Malta
        "Q32",  # Luxembourg
        "Q27",  # Ireland
        "Q189",  # Iceland
        "Q214",  # Slovakia
        "Q863",  # Tajikistan
        "Q813",  # Kyrgyzstan
        "Q880",  # Turkmenistan
    ],
    "MIDDLE_EAST_AND_NORTH_AFRICA": [
        "Q858",  # Syria
        "Q796",  # Iraq
        "Q794",  # Iran
        "Q851",  # Saudi Arabia
        "Q801",  # Israel
        "Q219060",  # Palestine
        "Q810",  # Jordan
        "Q822",  # Lebanon
        "Q805",  # Yemen
        "Q842",  # Oman
        "Q878",  # United Arab Emirates
        "Q817",  # Kuwait
        "Q398",  # Bahrain
        "Q846",  # Qatar
        "Q79",  # Egypt
        "Q1016",  # Libya
        "Q948",  # Tunisia
        "Q262",  # Algeria
        "Q1028",  # Morocco
        "Q1049",  # Sudan
        "Q6250",  # Western Sahara
    ],
    "NORTH_AMERICA": [
        "Q30",  # United States
        "Q16",  # Canada
        "Q96",  # Mexico
    ],
    "EAST_ASIA_AND_PACIFIC": [
        "Q148",  # China
        "Q17",  # Japan
        "Q884",  # South Korea
        "Q423",  # North Korea
        "Q408",  # Australia
        "Q664",  # New Zealand
        "Q252",  # Indonesia
        "Q928",  # Philippines
        "Q881",  # Vietnam
        "Q869",  # Thailand
        "Q833",  # Malaysia
        "Q334",  # Singapore
        "Q836",  # Myanmar
        "Q424",  # Cambodia
        "Q819",  # Laos
        "Q865",  # Taiwan
        "Q711",  # Mongolia
        "Q691",  # Papua New Guinea
        "Q712",  # Fiji
        "Q702",  # Micronesia
        "Q709",  # Marshall Islands
        "Q685",  # Solomon Islands
        "Q683",  # Tonga
        "Q672",  # Tuvalu
        "Q677",  # Vanuatu
        "Q921",  # Brunei
        "Q574",  # Timor-Leste
        "Q686",  # Palau
        "Q695",  # Kiribati
        "Q697",  # Nauru
        "Q699",  # Samoa
    ],
    "SOUTH_ASIA": [
        "Q668",  # India
        "Q843",  # Pakistan
        "Q902",  # Bangladesh
        "Q889",  # Afghanistan
        "Q854",  # Sri Lanka
        "Q837",  # Nepal
        "Q917",  # Bhutan
        "Q826",  # Maldives
    ],
    "LATIN_AMERICA_AND_CARIBBEAN": [
        "Q155",  # Brazil
        "Q414",  # Argentina
        "Q739",  # Colombia
        "Q717",  # Venezuela
        "Q298",  # Chile
        "Q419",  # Peru
        "Q736",  # Ecuador
        "Q750",  # Bolivia
        "Q733",  # Paraguay
        "Q77",  # Uruguay
        "Q241",  # Cuba
        "Q790",  # Haiti
        "Q786",  # Dominican Republic
        "Q766",  # Jamaica
        "Q804",  # Panama
        "Q800",  # Costa Rica
        "Q783",  # Honduras
        "Q774",  # Guatemala
        "Q792",  # El Salvador
        "Q811",  # Nicaragua
        "Q754",  # Trinidad and Tobago
        "Q757",  # Saint Vincent and the Grenadines
        "Q760",  # Grenada
        "Q763",  # Saint Lucia
        "Q769",  # Barbados
        "Q781",  # Antigua and Barbuda
        "Q784",  # Saint Kitts and Nevis
        "Q778",  # Bahamas
        "Q244",  # Belize
        "Q730",  # Guyana
        "Q747",  # Suriname
    ],
    "SUB_SAHARAN_AFRICA": [
        "Q1033",  # Nigeria
        "Q115",  # Ethiopia
        "Q974",  # Democratic Republic of Congo
        "Q258",  # South Africa
        "Q114",  # Kenya
        "Q924",  # Tanzania
        "Q1036",  # Uganda
        "Q117",  # Ghana
        "Q1029",  # Mozambique
        "Q916",  # Angola
        "Q1009",  # Cameroon
        "Q1019",  # Madagascar
        "Q1032",  # Niger
        "Q912",  # Mali
        "Q965",  # Burkina Faso
        "Q958401",  # South Sudan
        "Q1045",  # Somalia
        "Q954",  # Zimbabwe
        "Q1037",  # Rwanda
        "Q1041",  # Senegal
        "Q657",  # Chad
        "Q1006",  # Guinea
        "Q953",  # Zambia
        "Q986",  # Eritrea
        "Q1044",  # Sierra Leone
        "Q945",  # Togo
        "Q1014",  # Liberia
        "Q929",  # Central African Republic
        "Q1025",  # Mauritania
        "Q962",  # Benin
        "Q967",  # Burundi
        "Q971",  # Republic of Congo
        "Q1020",  # Malawi
        "Q1013",  # Lesotho
        "Q963",  # Botswana
        "Q1030",  # Namibia
        "Q1000",  # Gabon
        "Q983",  # Equatorial Guinea
        "Q977",  # Djibouti
        "Q970",  # Comoros
        "Q1011",  # Cabo Verde
        "Q1042",  # São Tomé and Príncipe
        "Q1046",  # Seychelles
        "Q1027",  # Mauritius
        "Q1050",  # Eswatini
        "Q1007",  # Guinea-Bissau
    ],
}


def get_country_qcodes_for_regions(regions: list[str]) -> list[str]:
    qcodes = []
    for region in regions:
        qcodes.extend(REGION_COUNTRY_QCODES.get(region, []))
    return list(dict.fromkeys(qcodes))  # deduplicate, preserve order
