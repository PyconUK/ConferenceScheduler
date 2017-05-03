import numpy as np
from collections import Counter
from conference_scheduler import scheduler


def test_valid_solution_has_no_violations(
    valid_solution, shape, sessions, slots, events
):
    violations = list(scheduler.constraint_violations(
        valid_solution, sessions, events, slots))
    assert len(violations) == 0


def test_unscheduled_event_has_violations(shape, sessions, slots, events):
    # solution with event 1 not scheduled
    solution = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, sessions, events, slots))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 1'
    ]


def test_multiple_event_schedule_has_violations(sessions, slots, events):
    # solution with event 0 scheduled twice
    solution = np.array([
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, sessions, events, slots))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 0'
    ]


def test_multiple_slot_schedule_has_violations(sessions, slots, events):
    # solution with slot 5 scheduled twice
    solution = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, sessions, events, slots))
    assert violations == ['Slot with multiple events scheduled - slot: 5']


def test_session_with_multiple_tags_has_violations(sessions, slots, events):
    # solution where events 0 and 2 are in same session but share no tag
    solution = np.array([
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, sessions, events, slots))
    assert violations == [
        'Dissimilar events schedule in same session - event: 0, slot: 3',
        'Dissimilar events schedule in same session - event: 2, slot: 4',
    ]


def test_event_scheduled_within_unavailability_has_violations(
    sessions, slots, events
):
    # solution where event 1 is incorrectly scheduled against event 0
    # as slots 2 and 6 both begin at 11:30
    solution = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, sessions, events, slots))
    assert violations == [
        'Event clashes with another event - event: 0 and event: 1'
    ]


def test_valid_solution_passes(valid_solution, sessions, slots, events):
    assert scheduler.is_valid_solution(
        valid_solution, sessions, events, slots)


def test_empty_solution_fails(sessions, slots, events):
    solution = []
    assert not scheduler.is_valid_solution(
        solution, sessions, events, slots)


def test_empty_schedule_fails(sessions, slots, events):
    schedule = []
    assert not scheduler.is_valid_schedule(schedule, sessions, slots, events)


def test_valid_schedule_passes(valid_schedule, sessions, slots, events):
    assert scheduler.is_valid_schedule(valid_schedule, sessions, slots, events)


def test_schedule_has_content(solution):
    assert len(solution) > 0


def test_all_events_scheduled(shape, solution):
    scheduled_events = [item[0] for item in solution]
    for event in range(shape.events):
        assert event in scheduled_events


def test_slots_scheduled_once_only(solution):
    for slot, count in Counter(item[1] for item in solution).items():
        assert count <= 1


def test_events_scheduled_once_only(solution):
    for event, count in Counter(item[0] for item in solution).items():
        assert count == 1
