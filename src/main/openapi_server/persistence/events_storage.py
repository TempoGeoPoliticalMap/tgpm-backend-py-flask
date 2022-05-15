# https://rdflib.github.io/sparqlwrapper/

from SPARQLWrapper import SPARQLWrapper, JSON

from openapi_server.mapper.event_mapper import event_dao_to_event

endpoint_url = "https://query.wikidata.org/sparql"

query = """#SELECT DISTINCT ?item ?itemLabel ?itemId ?point_in_time ?start_time ?end_time WHERE {
SELECT DISTINCT ?item ?itemLabel ?point_in_time ?start_time ?end_time WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P31 ?statement0.
      ?statement0 (ps:P31/(wdt:P279*)) wd:Q1139665.
    }
    LIMIT 10
  }
  OPTIONAL { ?item wdt:P1 ?itemId. }
  OPTIONAL { ?item wdt:P585 ?point_in_time. }
  OPTIONAL { ?item wdt:P580 ?start_time. }
  OPTIONAL { ?item wdt:P582 ?end_time. }
  OPTIONAL {  }
}"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % ("test", "debug")
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_event_dao_list():
    results = get_results(endpoint_url, query)
    return results["results"]

# for result in ["bindings"]:
#     event = event_dao_to_event(result)
#     print(result)

# if __name__ == '__main__':
#     get_results()
