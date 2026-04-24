from event_resolver.mapper.event_mapper import event_dao_to_event
from event_resolver.persistence.repository.events_storage import get_event_dao_list
from openapi_models.models.event import Event


def get_events():
    result: list[Event] = []

    for ed in get_event_dao_list()["bindings"]:
        result.append(event_dao_to_event(ed))

    return result
