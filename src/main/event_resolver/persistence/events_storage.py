# https://rdflib.github.io/sparqlwrapper/
from datetime import datetime
from datetime import timedelta

from SPARQLWrapper import SPARQLWrapper, JSON

# TODO TGPM-11 To add support for dates to be provided in the API request
date_format = "%Y-%m-%d"
today = datetime.now()
today_formatted = f'"{today.strftime(date_format)}"^^xsd:dateTime'
time_window = timedelta(days=30)
thirty_days_ago = today - time_window
thirty_days_ago_formatted = f'"{thirty_days_ago.strftime(date_format)}"^^xsd:dateTime'

endpoint_url = "https://query.wikidata.org/sparql"

# Query can be tested here: https://query.wikidata.org/
# SPARQL Docs: https://en.wikibooks.org/wiki/SPARQL/Expressions_and_Functions

events_query = (
    """SELECT DISTINCT ?item ?itemLabel ?itemDescription ?type ?start_time  WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en,fr,es". }
    
    VALUES ?type { wd:Q71266556 wd:Q2001676 wd:Q860251 wd:Q350604 wd:Q1139665 wd:Q858439 wd:Q5452198 wd:Q2618461 wd:Q47566 }
    
    # Main items by type
    ?item wdt:P31 ?type.
    
    # Optionally include subclasses if necessary
    OPTIONAL { ?item wdt:P31/wdt:P279 ?subType. ?subType wdt:P279* ?type. }
    
    OPTIONAL { ?item (wdt:P585) ?point_in_time. }
    OPTIONAL { ?item (wdt:P580) ?start_time_indicator. }
    #OPTIONAL { ?item (wdt:P582) ?end_time_indicator. }
    
    BIND(IF(BOUND(?start_time_indicator),?start_time_indicator,?point_in_time) AS ?start_time). 
    
    VALUES ?period_start_date { "2024-09-05"^^xsd:dateTime }
    VALUES ?period_end_date { "2024-12-05"^^xsd:dateTime }
    
    FILTER ( ?start_time >= ?period_start_date && ?start_time <= ?period_end_date)}
     
    ORDER BY DESC(?start_time) 
    LIMIT 100"""
)

query_event_countries = """SELECT DISTINCT ?item ?itemLabel ?country ?countryLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
  
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P31 ?statement0.
      ?statement0 (ps:P31/(wdt:P279*)) wd:Q1139665.
    }
    LIMIT 100
  }
  OPTIONAL { ?item wdt:P17 ?country. }
}"""


def get_results(endpoint_url, query):
    # TODO adjust user agent; see https://w.wiki/CX6
    user_agent = "WDQS-example Python/%s.%s" % ("test", "debug")
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_event_dao_list():
    results = get_results(endpoint_url, events_query)
    return results["results"]
