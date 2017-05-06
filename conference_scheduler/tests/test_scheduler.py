import pytest
import numpy as np
from collections import Counter
from conference_scheduler.resources import Slot
from conference_scheduler import scheduler
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


def test_demand_difference_schedule(slots, events):
    solution = scheduler.solution(
        events=events, slots=slots,
        objective_function=of.capacity_demand_difference
    )
    assert list(solution) == [(0, 3), (1, 4), (2, 6)]


def test_small_distance_from_other_schedule(slots, events):
    X_orig = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    schedule = scheduler.array_to_schedule(array=X_orig, slots=slots,
                                           events=events)
    solution = scheduler.solution(
        events=events, slots=slots,
        objective_function=of.number_of_changes,
        original_schedule=schedule,
    )
    assert list(solution) == [(0, 5), (1, 4), (2, 6)]

    X_orig = np.array([
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    schedule = scheduler.array_to_schedule(array=X_orig, slots=slots,
                                           events=events)
    solution = scheduler.solution(
        events=events, slots=slots,
        objective_function=of.number_of_changes,
        original_schedule=schedule,
    )
    assert list(solution) == [(0, 6), (1, 0), (2, 5)]


def test_unsolvable_raises_error(events):
    slots = [
        Slot(
            venue='Main Hall', starts_at='15-Sep-2016 09:30', duration=30,
            capacity=50, session="01 Morning A"
        )
    ]
    with pytest.raises(ValueError):
        scheduler.solution(events, slots)


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


# Testing the conversion between various forms of schedule output

def test_solution_to_array(valid_solution, valid_array, events, slots):
    array = scheduler.solution_to_array(valid_solution, events, slots)
    assert np.array_equal(array, valid_array)


def test_solution_to_schedule(valid_solution, valid_schedule, events, slots):
    schedule = scheduler.solution_to_schedule(valid_solution, events, slots)
    assert list(schedule) == valid_schedule


def test_schedule_to_array(valid_schedule, valid_array, events, slots):
    array = scheduler.schedule_to_array(valid_schedule, events, slots)
    assert np.array_equal(array, valid_array)


def test_array_to_schedule(valid_schedule, valid_array, events, slots):
    schedule = list(
        scheduler.array_to_schedule(valid_array, events, slots)
    )
    assert schedule == valid_schedule
