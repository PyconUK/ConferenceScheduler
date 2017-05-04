import numpy as np
from collections import Counter
from conference_scheduler import scheduler
from conference_scheduler.resources import ScheduledItem
from conference_scheduler.lp_problem import objective_functions as of


# Testing of the three output functions called by external programs

# Solution form
# There is most testing here since the scheduler.solution function is the one
# that sets up the pulp problem and returns the solution from pulp


def test_solution_has_content(solution):
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


# Array form
# Less testing needed here since it simply calls scheduler.solution and
# converts the result to array form


def test_array_has_content(array):
    assert len(array) > 0


def test_array_shape(array):
    assert array.shape == (3, 7)


def test_array_nonzero(array):
    nonzero = np.transpose(np.nonzero(array))
    assert len(nonzero) == 3


# Schedule form
# Similar to array form, there is less testsing here since it simply converts
# the output of scheduler.solution to schedule form


def test_schedule_has_content(schedule):
    assert len(schedule) > 0


def test_schedule_has_all_events(schedule, events):
    scheduled_events = [item.event for item in schedule]
    assert scheduled_events == list(events)


def test_valid_array_has_no_violations(
    valid_array, events, slots, sessions
):
    violations = list(scheduler.constraint_violations(
        events, slots, sessions, valid_array))
    assert len(violations) == 0


# Testing the conversion between various forms of schedule output


def test_schedule_to_array(valid_schedule, valid_array, events, slots):
    array = scheduler._schedule_to_array(valid_schedule, events, slots)
    assert np.array_equal(array, array)


def test_array_to_schedule(valid_schedule, valid_array, events, slots):
    schedule = list(
        scheduler._array_to_schedule(valid_array, events, slots)
    )
    assert schedule == valid_schedule


# Testing the validation of existing schedules against supplied constraints


def test_unscheduled_event_has_violations(events, slots, sessions):
    # array with event 1 not scheduled
    array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        events, slots, sessions, array))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 1'
    ]


def test_multiple_event_schedule_has_violations(events, slots, sessions):
    # array with event 0 scheduled twice
    array = np.array([
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        events, slots, sessions, array))
    assert violations == [
        'Event either not scheduled or scheduled multiple times - event: 0'
    ]


def test_multiple_slot_schedule_has_violations(events, slots, sessions):
    # array with slot 5 scheduled twice
    array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = list(scheduler.constraint_violations(
        events, slots, sessions, array))
    assert violations == ['Slot with multiple events scheduled - slot: 5']


def test_session_with_multiple_tags_has_violations(events, slots, sessions):
    # array where events 0 and 2 are in same session but share no tag
    array = np.array([
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    violations = list(scheduler.constraint_violations(
        events, slots, sessions, array))
    assert violations == [
        'Dissimilar events schedule in same session - event: 0, slot: 3',
        'Dissimilar events schedule in same session - event: 2, slot: 4',
    ]


def test_event_scheduled_within_unavailability_has_violations(
    events, slots, sessions
):
    # array where event 1 is incorrectly scheduled against event 0
    # as slots 2 and 6 both begin at 11:30
    array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    violations = list(scheduler.constraint_violations(
        events, slots, sessions, array))
    assert violations == [
        'Event clashes with another event - event: 0 and event: 1'
    ]


def test_valid_array_passes(valid_array, events, slots, sessions):
    assert scheduler.is_valid_array(
        events, slots, sessions, valid_array)


def test_empty_array_fails(events, slots, sessions):
    array = []
    assert not scheduler.is_valid_array(events, slots, sessions, array)


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
