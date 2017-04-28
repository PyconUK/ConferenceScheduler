import pytest
from conference_scheduler.resources import (
    Person, Room, Slot, Session, EventType, Event, Role, Demand,
    Unavailability
)


@pytest.fixture(scope="module")
def people():
    return {
        'alice': Person(name='Alice', max_chair_sessions=3),
        'bob': Person(name='Bob', max_chair_sessions=3),
        'charlie': Person(name='Charlie')
    }


@pytest.fixture(scope="module")
def event_types():
    return {
        'workshop': EventType(name='workshop'),
        'talk': EventType(name='talk')
    }


@pytest.fixture(scope="module")
def rooms(event_types):
    return (
        Room(
            name='Main Hall', capacity=500, suitability=event_types['talk']),
        Room(
            name='Room 1', capacity=50, suitability=event_types['workshop'])
    )


@pytest.fixture(scope="module")
def slots():
    return (
        Slot(starts_at='15-Sep-2016 09:30', ends_at='15-Sep-2016 10:00'),
        Slot(starts_at='15-Sep-2016 10:00', ends_at='15-Sep-2016 10:30'),
        Slot(starts_at='15-Sep-2016 11:30', ends_at='15-Sep-2016 12:00'),
        Slot(starts_at='15-Sep-2016 12:00', ends_at='15-Sep-2016 12:30'),
    )


@pytest.fixture(scope="module")
def sessions(slots):
    return (
        Session(slots=(slots[0], slots[1])),
        Session(slots=(slots[2], slots[3]))
    )


@pytest.fixture(scope="module")
def roles():
    return {
        'speaker': Role(name='speaker'),
        'leader': Role(name='leader'),
        'mentor': Role(name='mentor')
    }


@pytest.fixture(scope="module")
def events(event_types, roles, people):
    return (
        Event(
            name='Talk 1',
            event_type=event_types['talk'],
            roles={roles['speaker']: people['alice']}
        ),
        Event(
            name='Talk 2',
            event_type=event_types['talk'],
            roles={roles['speaker']: people['bob']}
        ),
        Event(
            name='Workshop 1',
            event_type=event_types['workshop'],
            roles={roles['leader']: people['charlie']}
        )
    )


@pytest.fixture(scope="module")
def demand(events):
    return (
        Demand(event=events['talk_1'], audience=300),
        Demand(event=events['talk_2'], audience=300),
        Demand(event=events['workshop_1'], audience=30),
    )


@pytest.fixture(scope="module")
def unavailability(people, slots):
    return (
        Unavailability(person=people['alice'], slot=slots[0]),
        Unavailability(person=people['alice'], slot=slots[1]),
        Unavailability(person=people['bob'], slot=slots[2]),
        Unavailability(person=people['bob'], slot=slots[3]),
    )
