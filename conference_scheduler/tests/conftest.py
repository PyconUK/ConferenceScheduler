import pytest
import numpy as np
from conference_scheduler.resources import (
    Person, Room, Slot, Session, EventType, Event, Role, Demand,
    Unavailability
)
from conference_scheduler import scheduler
from conference_scheduler import parameters


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
            name='Main Hall',
            capacity=500,
            suitability=[event_types['talk']]),
        Room(
            name='Room 2.32',
            capacity=50,
            suitability=[event_types['workshop']])
    )


@pytest.fixture(scope="module")
def slots(rooms):
    return (
        Slot(room=rooms[0], starts_at='15-Sep-2016 09:30', duration=30),
        Slot(room=rooms[0], starts_at='15-Sep-2016 10:00', duration=30),
        Slot(room=rooms[0], starts_at='15-Sep-2016 11:30', duration=30),
        Slot(room=rooms[0], starts_at='15-Sep-2016 12:00', duration=30),
        Slot(room=rooms[0], starts_at='15-Sep-2016 12:30', duration=30),
        Slot(room=rooms[1], starts_at='15-Sep-2016 09:30', duration=90),
        Slot(room=rooms[1], starts_at='15-Sep-2016 11:30', duration=90)
    )


@pytest.fixture(scope="module")
def sessions(slots):
    return (
        Session(slots=(slots[0], slots[1], slots[2])),
        Session(slots=(slots[3], slots[4])),
        Session(slots=(slots[5],)),
        Session(slots=(slots[6],)),
    )


@pytest.fixture(scope="module")
def roles():
    return {
        'speaker': Role(name='speaker'),
        'leader': Role(name='leader'),
        'mentor': Role(name='mentor')
    }


@pytest.fixture(scope="module")
def events(event_types, roles, people, slots):
    event1 = Event(
        name='Talk 1',
        event_type=event_types['talk'],
        duration=30,
        roles={roles['speaker']: people['alice']},
        tags=['community'],
        unavailability=[slots[0], slots[1]])
    event2 = Event(
        name='Talk 2',
        event_type=event_types['talk'],
        duration=30,
        roles={roles['speaker']: people['bob']},
        tags=['community', 'documentation'],
        unavailability=[slots[2], slots[3], event1])
    event3 = Event(
        name='Workshop 1',
        event_type=event_types['workshop'],
        duration=60,
        roles={roles['leader']: people['charlie']},
        tags=['documentation'],
        unavailability=[])
    return (event1, event2, event3)


@pytest.fixture(scope="module")
def demand(events):
    return (
        Demand(event=events['talk_1'], audience=300),
        Demand(event=events['talk_2'], audience=300),
        Demand(event=events['workshop_1'], audience=30),
    )


@pytest.fixture(scope='module')
def shape(events, slots):
    return parameters.Shape(len(events), len(slots))


@pytest.fixture(scope='module')
def tag_array(events):
    return parameters.tag_array(events)


@pytest.fixture(scope='module')
def session_array(sessions):
    return parameters.session_array(sessions)


@pytest.fixture(scope='module')
def slot_availability_array(events, slots):
    return parameters.slot_availability_array(events, slots)


@pytest.fixture(scope='module')
def event_availability_array(events, slots):
    return parameters.event_availability_array(events)


@pytest.fixture(scope='module')
def X(shape):
    return parameters.variables(shape)


@pytest.fixture(scope='module')
def solution(shape, events, slots, sessions):
    return [
        item for item in scheduler.solution(shape, events, slots, sessions)
    ]


@pytest.fixture(scope='module')
def schedule(events, slots):
    return [item for item in scheduler.schedule(events, slots)]


@pytest.fixture(scope='module')
def valid_solution():
    return np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
