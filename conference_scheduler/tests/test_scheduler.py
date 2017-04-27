import pulp
from conference_scheduler.resources import Person, Room, Slot
from conference_scheduler import scheduler

people = (
    Person(name='Alice'),
    Person(name='Bob'),
    Person(name='Charlie')
)

rooms = (
    Room(name='Main Hall', capacity=500),
    Room(name='Room 1', capacity=50)
)

slots = (
    Slot(starts_at='15-Sep-2016 09:30', ends_at='15-Sep-2016 10:00'),
    Slot(starts_at='15-Sep-2016 10:00', ends_at='15-Sep-2016 10:30')
)


def test_is_valid_schedule():
    # Test empty schedule
    schedule = tuple()
    problem = pulp.LpProblem()
    assert not scheduler.is_valid_schedule(schedule, problem)


def test_schedule():
    pass
