from .utils import element_from_neighbourhood, get_initial_array
import warnings

def hill_climber(objective_function,
                 initial_array,
                 lower_bound=-float('inf'),
                 max_iterations=10 ** 3):
    """
    Implement a basic hill climbing algorithm.

    Has two stopping conditions:

    1. Maximum number of iterations;
    2. A known lower bound, a none is passed then this is not used.
    """

    X = initial_array

    iterations = 0
    current_energy = objective_function(X)

    while current_energy > lower_bound and iterations <= max_iterations:

        iterations += 1
        candidate = element_from_neighbourhood(X)
        candidate_energy = objective_function(candidate)

        if candidate_energy < current_energy:

            X = candidate
            current_energy = candidate_energy

    if lower_bound > -float('inf') and current_energy != lower_bound:
        warnings.warn(f"Lower bound {lower_bound} not achieved after {max_iterations} iterations")

    return X
