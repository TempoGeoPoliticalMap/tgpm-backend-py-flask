from typing import List

from openapi_server.persistence.events_storage import get_event_dao_list
from openapi_server.mapper.event_mapper import event_dao_to_event
from openapi_server.models import Event


def get_events(types=None, regions=None, countries=None, timeslot_start=None, timeslot_end=None):
    result: List[Event] = []

    for ed in get_event_dao_list()["bindings"]:
        result.append(event_dao_to_event(ed))

    return result

# if __name__ == '__main__':
#     get_events()
#
