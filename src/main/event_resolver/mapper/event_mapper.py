from datetime import datetime
from models import Event
from wikidata_class_name import get_wikidata_event_type_name

now = datetime.now()
date_format = "%Y-%m-%dT%H:%M:%SZ"


def event_dao_to_event(input_dict):
    event = Event()

    # TODO TGPM-12 To add filtration by Event Type; now it's hardcoded
    event.type = get_wikidata_event_type_name(
        input_dict["itemType"]["value"].replace("http://www.wikidata.org/entity/", "")
    )
    event.wikidata_id = input_dict["item"]["value"]
    event.name = input_dict["itemLabel"]["value"]
    event.start_time = input_dict["startTime"]["value"]

    if now < datetime.strptime(input_dict["startTime"]["value"], date_format):
        event.time_state_relative_to_now = "FUTURE"
    else:
        event.time_state_relative_to_now = "STARTED"

    return event
