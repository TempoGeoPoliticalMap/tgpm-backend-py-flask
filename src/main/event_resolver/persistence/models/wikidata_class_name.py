def get_wikidata_event_type_name(code):
    name = {
        "Q71266556": "Warfare and armed conflicts",
        "Q2001676": "Offensive",
        "Q860251": "Urban warfare",
        "Q350604": "Armed conflict",
        "Q1139665": "Political murder",
        "Q858439": "Presidential election",
        "Q5452198": "First-order election",
        "Q2618461": "Legislative election",
        "Q47566": "United States presidential election",
    }
    return name.get(code, "Unknown")
