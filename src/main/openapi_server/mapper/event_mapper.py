from datetime import datetime
from dateutil import parser
from openapi_server.models import Event

now = datetime.now()


def event_dao_to_event(input_dict):
    event = Event()
    event.wikidata_id = input_dict["item"]["value"].replace(
        "http://www.wikidata.org/entity/", ""
    )
    event.name = input_dict["itemLabel"]["value"]

    if "start_time_indicator" in input_dict:
        event.start_time = input_dict["start_time_indicator"]["value"]

    if "end_time" in input_dict:
        event.end_time = input_dict["end_time"]["value"]
        # TODO TGPM-11 When this story will be implemented, the conditions below need to be extended to address
        #  additional cases, i.e. future events
        if parser.parse(event.end_time).timestamp() < now.timestamp():
            event.time_state_relative_to_now = "PAST"
        else:
            event.time_state_relative_to_now = "ONGOING"
    else:
        event.time_state_relative_to_now = "ONGOING"

    # TODO TGPM-12 To add filtration by Event Type; now it's hardcoded
    event.type = "WARFARE_AND_ARMED_CONFLICTS"

    return event
