# https://rdflib.github.io/sparqlwrapper/

from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query_events = """SELECT DISTINCT ?item ?itemLabel ?itemDescription ?time_indicator ?start_time_indicator ?end_time  WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,fr,ge,es". }
  
  #VALUES ?type { wd:Q71266556 wd:Q1139665 }
  #VALUES ?type { wd:Q71266556 } ## ->136
  #VALUES ?type { wd:Q1139665 } ## ->6
  ?item p:P31 ?statement0.
  #?statement0 (ps:P31/(wdt:P279*)) ?type.
  #?item wdt:P31/wdt:P279* ?type.
  #?statement0 (ps:P31/(wdt:P279*)) wd:Q71266556. ## 'warfare and armed conflicts' ->136
  ?statement0 (ps:P31/(wdt:P279*)) wd:Q1139665.  ## 'political murder'            ->  6
  
  ?item (wdt:P585|wdt:P580) ?start_time_indicator.
  
  OPTIONAL { ?item wdt:P582 ?end_time. }

  ?item (wdt:P625|wdt:P276|wdt:17) ?location_indicator.
  
  OPTIONAL { ?item wdt:P625 ?coordinate_location. }
  OPTIONAL { ?item wdt:P276 ?location. }
  OPTIONAL { ?item wdt:P17 ?country. }

  VALUES ?period_start_date { "2000-05-15"^^xsd:dateTime }
  VALUES ?period_end_date { "2015-05-23"^^xsd:dateTime }
  FILTER ((?start_time_indicator >= ?period_start_date && ?start_time_indicator <= ?period_end_date) || 
          (?end_time >= ?period_start_date && ?end_time <= ?period_end_date) ||
          (?start_time_indicator <= ?period_start_date && ?end_time >= ?period_end_date)
         )
} 
ORDER BY ASC(?start_time_indicator) ASC(?end_time)
LIMIT 500"""

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
    user_agent = "WDQS-example Python/%s.%s" % ("test", "debug")
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_event_dao_list():
    results = get_results(endpoint_url, query_events)
    return results["results"]


# for result in ["bindings"]:
#     event = event_dao_to_event(result)
#     print(result)

# if __name__ == '__main__':
#     get_results()
