from .utils import element_from_neighbourhood, get_initial_array
import numpy as np
import warnings

def simulated_annealing(objective_function,
                        initial_array,
                        initial_temperature=10 ** 4,
                        cooldown_rate=0.7,
                        lower_bound=-float('inf'),
                        max_iterations=10 ** 3):
    """
    Implement a simulated annealing algorithm with exponential cooling

    Has two stopping conditions:

    1. Maximum number of iterations;
    2. A known lower bound, a none is passed then this is not used.

    Note that starting with an initial_temperature corresponds to a hill
    climbing algorithm
    """

    X = initial_array
    best_X = X

    iterations = 0
    current_energy = objective_function(X)
    best_energy = current_energy
    temperature = initial_temperature

    while current_energy > lower_bound and iterations <= max_iterations:

        iterations += 1
        candidate = element_from_neighbourhood(X)
        candidate_energy = objective_function(candidate)

        delta = candidate_energy - current_energy

        if delta < 0:
            best_energy = candidate_energy
            best_X = candidate

        if delta < 0 or (temperature > 0 and
                         np.random.random() < np.exp(-delta / temperature)):
            X = candidate
            current_energy = candidate_energy

        temperature *= (cooldown_rate) ** iterations

    if lower_bound > -float('inf') and current_energy != lower_bound:
        warnings.warn(f"Lower bound {lower_bound} not achieved after {max_iterations} iterations")

    return best_X
