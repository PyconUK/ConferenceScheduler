import numpy as np
from conference_scheduler.lp_problem import objective_functions as of
from conference_scheduler.validator import array_violations
from conference_scheduler.heuristics import hill_climber


def test_hill_climber_for_valid_solution(slots, events):

    def objective_function(array):
        return len(list(array_violations(array, events, slots)))

    array = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    assert objective_function(array) == 2

    np.random.seed(0)
    X = hill_climber(initial_array=array,
                     lower_bound=0,
                     objective_function=objective_function,
                     max_iterations=150)

    assert objective_function(X) == 0


def test_hill_climber_for_valid_solution_with_low_max_iterations(
    slots, events
):

    def objective_function(array):
        return len(list(array_violations(array, events, slots)))

    array = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    assert objective_function(array) == 2

    np.random.seed(0)
    X = hill_climber(initial_array=array,
                     objective_function=objective_function,
                     max_iterations=1)

    assert objective_function(X) == 1


def test_hill_climber_for_valid_solution_warning_raised(slots, events):
    """
    Test that a warning is given if a lower bound is passed and not reached in
    given number of iterations.
    """
    def objective_function(array):
        return len(list(array_violations(array, events, slots)))

    array = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    assert objective_function(array) == 2

    np.random.seed(0)
    X = hill_climber(initial_array=array,
                     objective_function=objective_function,
                     lower_bound=0,
                     max_iterations=1)

    assert objective_function(X) == 1
    # TODO Check warning is raised


def test_hill_climber_for_objective_function(slots, events):

    def objective_function(array):
        return of.capacity_demand_difference(slots, events, array)

    array = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    assert objective_function(array) == -400

    np.random.seed(0)
    X = hill_climber(initial_array=array,
                     objective_function=objective_function,
                     max_iterations=10)

    assert objective_function(X) == -440
