Use heuristics
==============

The linear programming approach is guaranteed to give an optimal solution,
however this can be quite expensive computationally. It is possible to use a
heuristic approach that probabilistically searches through the solution space.

Here is how to do this with a hill climbing algorithm::

    >>> import conference_scheduler.heuristics as heu
    >>> heuristic = heu.hill_climber
    >>> scheduler.heuristic(events=events, slots=slots, algorithm=heuristic) # doctest: +SKIP

A simulated annealing algorithm is also implemented::

    >>> heuristic = heu.simulated_annealing
    >>> scheduler.heuristic(events=events, slots=slots, algorithm=heuristic) # doctest: +SKIP
