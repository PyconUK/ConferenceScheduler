import pulp
from conference_scheduler.resources import Person, Room, Slot, Session, EventType, Event, Role
from conference_scheduler import scheduler

people = {
    'alice': Person(name='Alice'),
    'bob': Person(name='Bob'),
    'charlie': Person(name='Charlie')
}

event_types = {
    'workshop': EventType(name='workshop'),
    'talk': EventType(name='talk')
}


rooms = {
    'main_hall': Room(name='Main Hall', capacity=500, suitability=event_types['talk']),
    'room_1': Room(name='Room 1', capacity=50, suitability=event_types['workshop'])
}

slots = (
    Slot(starts_at='15-Sep-2016 09:30', ends_at='15-Sep-2016 10:00'),
    Slot(starts_at='15-Sep-2016 10:00', ends_at='15-Sep-2016 10:30'),
    Slot(starts_at='15-Sep-2016 11:30', ends_at='15-Sep-2016 12:00'),
    Slot(starts_at='15-Sep-2016 12:00', ends_at='15-Sep-2016 12:30'),
)

sessions = (
    Session(slots=(slots[0], slots[1])),
    Session(slots=(slots[2], slots[3]))
)


roles = {
    'speaker': Role(name='speaker'),
    'leader': Role(name='leader'),
    'mentor': Role(name='mentor')
}

events = (
    Event(name='Talk 1', event_type=event_types['talk'], roles={roles['speaker']: people['alice']}),
    Event(name='Talk 2', event_type=event_types['talk'], roles={roles['speaker']: people['bob']}),
    Event(name='Workshop 1', event_type=event_types['workshop'], roles={roles['leader']: people['charlie']})
)


def test_is_valid_schedule():
    # Test empty schedule
    schedule = tuple()
    problem = pulp.LpProblem()
    assert not scheduler.is_valid_schedule(schedule, problem)


def test_schedule():
    pass
