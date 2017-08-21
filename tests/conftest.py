from datetime import datetime
import pytest
import numpy as np
from conference_scheduler.resources import (
    Slot, Event, ScheduledItem, Shape
)
from conference_scheduler import scheduler
from conference_scheduler.lp_problem import utils as lpu


@pytest.fixture(scope="module")
def slots():
    return (
        Slot(venue='Room 1', starts_at=datetime(2016, 9, 15, 9, 30),
             duration=30, capacity=50, session="01 Morning A"),
        Slot(venue='Room 1', starts_at=datetime(2016, 9, 15, 10, 3),
             duration=30, capacity=50, session="01 Morning A"),
        Slot(venue='Room 1', starts_at=datetime(2016, 9, 15, 11, 30),
             duration=30, capacity=50, session="01 Morning A"),
        Slot(venue='Room 1', starts_at=datetime(2016, 9, 15, 12, 0),
             duration=30, capacity=10, session="02 Afternoon A"),
        Slot(venue='Room 1', starts_at=datetime(2016, 9, 15, 12, 30),
             duration=30, capacity=50, session="02 Afternoon A"),
        Slot(venue='Room 2', starts_at=datetime(2016, 9, 15, 9, 30),
             duration=90, capacity=200, session="03 Morning B"),
        Slot(venue='Room 2', starts_at=datetime(2016, 9, 15, 11, 30),
             duration=90, capacity=200, session="04 Afternoon B")
    )


@pytest.fixture(scope="module")
def events(slots):
    event1 = Event(
        name='Talk 1',
        duration=30,
        tags=['community'],
        unavailability=[slots[0], slots[1]],
        demand=30)
    event2 = Event(
        name='Talk 2',
        duration=30,
        tags=['community', 'documentation'],
        unavailability=[slots[2], slots[3], event1],
        demand=500)
    event3 = Event(
        name='Workshop 1',
        duration=60,
        tags=['documentation'],
        unavailability=[],
        demand=20)
    return (event1, event2, event3)


@pytest.fixture(scope='module')
def shape(events, slots):
    return Shape(len(events), len(slots))


@pytest.fixture(scope='module')
def tag_array(events):
    return lpu.tag_array(events)


@pytest.fixture(scope='module')
def session_array(slots):
    return lpu.session_array(slots)


@pytest.fixture(scope='module')
def X(shape):
    return lpu.variables(shape)


@pytest.fixture(scope='module')
def solution(events, slots):
    return list(scheduler.solution(events, slots))


@pytest.fixture(scope='module')
def array(events, slots):
    return scheduler.array(events, slots)


@pytest.fixture(scope='module')
def schedule(events, slots):
    return list(scheduler.schedule(events, slots))


@pytest.fixture(scope='module')
def valid_solution():
    return (
        (0, 2),
        (1, 4),
        (2, 5)
    )


@pytest.fixture(scope='module')
def valid_array():
    return np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])


@pytest.fixture(scope='module')
def valid_schedule(events, slots):
    return [
        ScheduledItem(event=events[0], slot=slots[2]),
        ScheduledItem(event=events[1], slot=slots[4]),
        ScheduledItem(event=events[2], slot=slots[5])
    ]
