from .utils import element_from_neighbourhood, get_initial_array
import warnings

def hill_climber(objective_function,
                 initial_array,
                 lower_bound=-float('inf'),
                 acceptance_criteria=None,
                 max_iterations=10 ** 3):
    """
    Implement a basic hill climbing algorithm.

    Has two stopping conditions:

    1. Maximum number of iterations;
    2. A known lower bound, a none is passed then this is not used.

    If acceptance_criteria (a callable) is not None then this is used to obtain
    an upper bound on some other measure (different to the objective function).
    In practice this is used when optimising the objective function to ensure
    that we don't accept a solution that improves the objective function but tht
    adds more constraint violations.
    """

    X = initial_array
    if acceptance_criteria is not None:
        acceptance_bound = acceptance_criteria(X)

    iterations = 0
    current_energy = objective_function(X)

    while current_energy > lower_bound and iterations <= max_iterations:

        iterations += 1
        candidate = element_from_neighbourhood(X)
        candidate_energy = objective_function(candidate)

        if (candidate_energy < current_energy and
            (acceptance_criteria is None or
             acceptance_criteria(candidate) <= acceptance_bound)):

            X = candidate
            current_energy = candidate_energy

    if lower_bound > -float('inf') and current_energy != lower_bound:
        warnings.warn(f"Lower bound {lower_bound} not achieved after {max_iterations} iterations")

    return X
