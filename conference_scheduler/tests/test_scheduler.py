from conference_scheduler.resources import (
    Person, Room, Slot, Session, EventType, Event, Role, Demand,
    Unavailability
)
from conference_scheduler import scheduler


def test_is_valid_schedule(people):
    # Test empty schedule
    schedule = tuple()
    assert not scheduler.is_valid_schedule(schedule)


def test_schedule():
    pass
