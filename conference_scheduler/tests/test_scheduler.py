from collections import Counter
from conference_scheduler import scheduler


def test_is_valid_schedule(people):
    # Test empty schedule
    schedule = tuple()
    assert not scheduler.is_valid_schedule(schedule)


def test_room_slot(events, rooms, slots, schedule):
    # A room may only have a maximum of one event scheduled in any time slot
    scheduled = Counter([(item.room.name, item.slot) for item in schedule])
    for item, count in scheduled.items():
        assert count <= 1


def test_room_suitable(events, rooms, slots, schedule):
    # A room may only be scheduled to host an event for which it is deemed
    # suitable
    for item in schedule:
        assert item.event.event_type in item.room.suitability


def test_event_once(events, rooms, slots, schedule):
    # An event may only be scheduled in one combination of room and time slot
    assert len(schedule) == len(events)
    scheduled_events = set([item.event.name for item in schedule])
    assert scheduled_events == set([event.name for event in events])
