from event_resolver.service import events_service


def v1_events_get():
    result = events_service.get_events()
    return [event.to_dict() for event in result]
