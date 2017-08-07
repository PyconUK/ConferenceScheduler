import numpy as np
from conference_scheduler.heuristics import utils as hu


# Tests for array form

def test_neighbourhood_move_to_unused():
    array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    np.random.seed(0)
    X = hu.element_from_neighbourhood(array)
    expected_array = np.array([
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    assert np.array_equal(X, expected_array)

def test_neighbourhood_swap_events():
    array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    np.random.seed(35)
    X = hu.element_from_neighbourhood(array)
    expected_array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    assert np.array_equal(X, expected_array)

def test_get_initial_array(events, slots):
    X = hu.get_initial_array(events=events, slots=slots, seed=0)
    expected_array = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0]
    ])
    assert np.array_equal(X, expected_array)

    X = hu.get_initial_array(events=events, slots=slots, seed=1)
    expected_array = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    assert np.array_equal(X, expected_array)
