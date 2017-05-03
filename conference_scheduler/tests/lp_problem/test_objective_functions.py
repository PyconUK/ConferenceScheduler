import numpy as np
from conference_scheduler.lp_problem import objective_functions as of


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
