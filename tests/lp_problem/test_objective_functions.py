import numpy as np
from conference_scheduler.lp_problem import objective_functions as of
from conference_scheduler.converter import array_to_schedule


def test_capacity_demand_difference(slots, events, X):
    function = of.capacity_demand_difference(slots, events, X)
    assert len(function) == 21


def test_capacity_demand_difference_with_examples(slots, events):
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    overflow = of.capacity_demand_difference(slots, events, X)
    assert overflow == -400

    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0]
    ])
    overflow = of.capacity_demand_difference(slots, events, X)
    assert overflow == -440


def test_number_of_changes(slots, events):
    X_orig = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    schedule = list(array_to_schedule(array=X_orig, slots=slots,
                                      events=events))

    assert of.number_of_changes(slots, events, schedule, X_orig) == 0

    X_new = np.array([
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    assert of.number_of_changes(slots, events, schedule, X_new) == 2

    X_new = np.array([
        [0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    assert of.number_of_changes(slots, events, schedule, X_new) == 7
