from typing import List

from event_resolver.mapper.event_mapper import event_dao_to_event

from models import Event
from events_storage import get_event_dao_list


def get_events():
    result: List[Event] = []

    for ed in get_event_dao_list()["bindings"]:
        result.append(event_dao_to_event(ed))

    return result
