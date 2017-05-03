import numpy as np
from collections import Counter
from conference_scheduler import scheduler
from conference_scheduler.resources import ScheduledItem
from conference_scheduler.lp_problem import objective_functions as of


def test_valid_solution_has_no_violations(
    valid_solution, events, slots, sessions
):
    violations = list(scheduler.constraint_violations(
        valid_solution, events, slots, sessions))
    assert len(violations) == 0


def test_unscheduled_event_has_violations(events, slots, sessions):
    # solution with event 1 not scheduled
    solution = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, events, slots, sessions))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 1'
    ]


def test_multiple_event_schedule_has_violations(events, slots, sessions):
    # solution with event 0 scheduled twice
    solution = np.array([
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, events, slots, sessions))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 0'
    ]


def test_multiple_slot_schedule_has_violations(events, slots, sessions):
    # solution with slot 5 scheduled twice
    solution = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, events, slots, sessions))
    assert violations == ['Slot with multiple events scheduled - slot: 5']


def test_session_with_multiple_tags_has_violations(events, slots, sessions):
    # solution where events 0 and 2 are in same session but share no tag
    solution = np.array([
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, events, slots, sessions))
    assert violations == [
        'Dissimilar events schedule in same session - event: 0, slot: 3',
        'Dissimilar events schedule in same session - event: 2, slot: 4',
    ]


def test_event_scheduled_within_unavailability_has_violations(
    events, slots, sessions
):
    # solution where event 1 is incorrectly scheduled against event 0
    # as slots 2 and 6 both begin at 11:30
    solution = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    violations = list(scheduler.constraint_violations(
        solution, events, slots, sessions))
    assert violations == [
        'Event clashes with another event - event: 0 and event: 1'
    ]


def test_valid_solution_passes(valid_solution, events, slots, sessions):
    assert scheduler.is_valid_solution(
        valid_solution, events, slots, sessions)


def test_empty_solution_fails(events, slots, sessions):
    solution = []
    assert not scheduler.is_valid_solution(
        solution, events, slots, sessions)


def test_schedule_to_solution(valid_schedule, valid_solution, events, slots):
    solution = scheduler._schedule_to_solution(valid_schedule, events, slots)
    assert np.array_equal(solution, valid_solution)


def test_solution_to_schedule(valid_schedule, valid_solution, events, slots):
    schedule = list(
        scheduler._solution_to_schedule(valid_solution, events, slots)
    )
    assert schedule == valid_schedule


def test_empty_schedule_fails(events, slots, sessions):
    schedule = []
    assert not scheduler.is_valid_schedule(schedule, events, slots, sessions)


def test_valid_schedule_passes(valid_schedule, events, slots, sessions):
    assert scheduler.is_valid_schedule(valid_schedule, events, slots, sessions)


def test_schedule_unscheduled_event_has_violations(events, slots, sessions):
    # schedule with event 1 not scheduled
    schedule = (
        ScheduledItem(event=events[0], slot=slots[2]),
        ScheduledItem(event=events[2], slot=slots[5])
    )
    violations = list(scheduler.schedule_violations(
        schedule, events, slots, sessions))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 1'
    ]


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


def test_optimal_schedule(slots, events, sessions):
    solution = scheduler.solution(
            events=events, slots=slots, sessions=sessions,
            objective_function=of.capacity_demand_difference)
    assert list(solution) == [(0, 3), (1, 4), (2, 0)]
