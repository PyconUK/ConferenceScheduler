import numpy as np
from conference_scheduler import validator
from conference_scheduler.resources import ScheduledItem


# Tests for array form


def test_unscheduled_event_has_violations(events, slots):
    # array with event 1 not scheduled
    array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(validator.array_violations(array, events, slots))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 1'
    ]


def test_multiple_event_schedule_has_violations(events, slots):
    # array with event 0 scheduled twice
    array = np.array([
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(validator.array_violations(array, events, slots))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 0'
    ]


def test_multiple_slot_schedule_has_violations(events, slots):
    # array with slot 5 scheduled twice
    array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(validator.array_violations(array, events, slots))
    assert violations == ['Slot with multiple events scheduled - slot: 5']


def test_session_with_multiple_tags_has_violations(events, slots):
    # array where events 0 and 2 are in same session but share no tag
    array = np.array([
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    violations = list(validator.array_violations(array, events, slots))
    assert violations == [
        'Dissimilar events schedule in same session - event: 0, slot: 3',
        'Dissimilar events schedule in same session - event: 2, slot: 4',
        'Event scheduled when not available - event: 2, slot: 4',
    ]


def test_event_scheduled_within_unavailability_has_violations(events, slots):
    # array where event 1 is incorrectly scheduled against event 0
    # as slots 2 and 6 both begin at 11:30
    array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(validator.array_violations(array, events, slots))
    assert violations == [
        'Event clashes with another event - event: 0 and event: 1'
    ]


def test_valid_array_passes(valid_array, events, slots):
    assert validator.is_valid_array(valid_array, events, slots)


def test_empty_array_fails(events, slots):
    array = []
    assert not validator.is_valid_array(array, events, slots)


# Tests for solution form


def test_empty_solution_fails(events, slots):
    assert not validator.is_valid_solution([], events, slots)


def test_valid_solution_passes(valid_solution, events, slots):
    assert validator.is_valid_solution(valid_solution, events, slots)


def test_solution_unscheduled_event_has_violations(events, slots):
    # solution with event 1 not schedule
    solution = [(0, 2), (2, 5)]
    violations = list(validator.solution_violations(solution, events, slots))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 1'
    ]


# Tests for schedule form


def test_empty_schedule_fails(events, slots):
    schedule = []
    assert not validator.is_valid_schedule(schedule, events, slots)


def test_valid_schedule_passes(valid_schedule, events, slots):
    assert validator.is_valid_schedule(valid_schedule, events, slots)


def test_schedule_unscheduled_event_has_violations(events, slots):
    # schedule with event 1 not scheduled
    schedule = (
        ScheduledItem(event=events[0], slot=slots[2]),
        ScheduledItem(event=events[2], slot=slots[5])
    )
    violations = list(validator.schedule_violations(schedule, events, slots))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 1'
    ]
