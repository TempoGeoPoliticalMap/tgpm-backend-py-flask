from openapi_server.models import Event


def event_dao_to_event(input_dict):
    event = Event()
    event.wikidata_id = input_dict["item"]["value"].replace(
        "http://www.wikidata.org/entity/", ""
    )
    event.name = input_dict["itemLabel"]["value"]

    if "point_in_time" in input_dict:
        event.start_time = input_dict["point_in_time"]["value"]
    elif "start_time" in input_dict:
        event.start_time = input_dict["start_time"]["value"]

    if "end_time" in input_dict:
        event.end_time = input_dict["end_time"]["value"]

    return event
