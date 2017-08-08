"""Compute a schedule in one of three forms, convert a schedule between forms
and compute the difference between .

A schedule can be represented in one of three forms:

    * solution: a list of tuples of event index and slot index
      for each scheduled item
    * array: a numpy array with rows for events and columns for slots
    * schedule: a generator for a list of ScheduledItem instances
"""

import pulp
import numpy as np
import conference_scheduler.lp_problem as lp
import conference_scheduler.heuristics as heu
import conference_scheduler.validator as val
from conference_scheduler.resources import (
    ScheduledItem, Shape, ChangedEventScheduledItem, ChangedSlotScheduledItem
)

# __all__ is defined so that we can control the order in which the functions
# are documented by sphinx.
__all__ = [
    'solution', 'array', 'schedule', 'solution_to_array',
    'solution_to_schedule', 'schedule_to_array', 'array_to_schedule',
    'event_schedule_difference', 'slot_schedule_difference']


# Functions to compute a schedule

def heuristic(events,
              slots,
              objective_function=None,
              algorithm=heu.hill_climber,
              initial_solution_algorithm_kwargs={},
              objective_function_algorithm_kwargs={},
              **kwargs):
    """
    Compute a schedule using a heuristic

    Parameters
    ----------
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances
    algorithm : callable
       a heuristic algorithm from conference_scheduler.heuristics
    initial_solution_algorithm_kwargs : dict
       kwargs for the heuristic algorithm for the initial solution
    objective_function_algorithm_kwargs : dict
       kwargs for the heuristic algorithm for the objective function (if
       necessary.
    objective_function: callable
        from lp_problem.objective_functions
    kwargs : keyword arguments
        arguments for the objective function

    Returns
    -------
    list
        A list of tuples giving the event and slot index (for the given
        events and slots lists) for all scheduled items.

    Example
    -------
    For a solution where

        * event 0 is scheduled in slot 1
        * event 1 is scheduled in slot 4
        * event 2 is scheduled in slot 5

    the resulting list would be::

        [(0, 1), (1, 4), (2, 5)]
    """
    X = heu.get_initial_array(events=events, slots=slots)

    def count_violations(array):
        return len(list(val.array_violations(array, events, slots)))

    X = algorithm(initial_array=X,
                  objective_function=count_violations,
                  lower_bound=0,
                  **initial_solution_algorithm_kwargs)

    if objective_function is not None:

        def func(array):
            return objective_function(
                events=events, slots=slots, X=array, **kwargs)

        X = algorithm(initial_array=X,
                      objective_function=func,
                      **objective_function_algorithm_kwargs)

    return list(zip(*np.nonzero(X)))


def solution(events, slots, objective_function=None, solver=None, **kwargs):
    """Compute a schedule in solution form

    Parameters
    ----------
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances
    solver : pulp.solver
        a pulp solver
    objective_function: callable
        from lp_problem.objective_functions
    kwargs : keyword arguments
        arguments for the objective function

    Returns
    -------
    list
        A list of tuples giving the event and slot index (for the given
        events and slots lists) for all scheduled items.

    Example
    -------
    For a solution where

        * event 0 is scheduled in slot 1
        * event 1 is scheduled in slot 4
        * event 2 is scheduled in slot 5

    the resulting list would be::

        [(0, 1), (1, 4), (2, 5)]
    """
    shape = Shape(len(events), len(slots))
    problem = pulp.LpProblem()
    X = lp.utils.variables(shape)

    for constraint in lp.constraints.all_constraints(
        events, slots, X, 'lpsum'
    ):
        problem += constraint.condition

    if objective_function is not None:
        problem += objective_function(events=events, slots=slots, X=X,
                                      **kwargs)

    status = problem.solve(solver=solver)
    if status == 1:
        return [item for item, variable in X.items() if variable.value() > 0]
    else:
        raise ValueError('No valid solution found')


def array(events, slots, objective_function=None, solver=None, **kwargs):
    """Compute a schedule in array form

    Parameters
    ----------
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances
    objective_function : callable
        from lp_problem.objective_functions

    Returns
    -------
    np.array
        An E by S array (X) where E is the number of events and S the
        number of slots. Xij is 1 if event i is scheduled in slot j and
        zero otherwise

    Example
    -------
    For 3 events, 7 slots and a solution where

        * event 0 is scheduled in slot 1
        * event 1 is scheduled in slot 4
        * event 2 is scheduled in slot 5

    the resulting array would be::

        [[0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 1, 0]]
    """
    return solution_to_array(
        solution(events, slots, objective_function, solver=solver, **kwargs),
        events, slots
    )


def schedule(events, slots, objective_function=None, solver=None, **kwargs):
    """Compute a schedule in schedule form

    Parameters
    ----------
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances
    solver : pulp.solver
        a pulp solver
    objective_function : callable
        from lp_problem.objective_functions
    kwargs : keyword arguments
        arguments for the objective function

    Returns
    -------
    list
        A list of instances of :py:class:`resources.ScheduledItem`
    """
    return solution_to_schedule(
        solution(events, slots, objective_function, solver=solver, **kwargs),
        events, slots
    )


# Functions to convert the schedule from one form to another

def solution_to_array(solution, events, slots):
    """Convert a schedule from solution to array form

    Parameters
    ----------
    solution : list or tuple
        of tuples of event index and slot index for each scheduled item
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances

    Returns
    -------
    np.array
        An E by S array (X) where E is the number of events and S the
        number of slots. Xij is 1 if event i is scheduled in slot j and
        zero otherwise

    Example
    -------
    For For 3 events, 7 slots and the solution::

        [(0, 1), (1, 4), (2, 5)]

    The resulting array would be::

        [[0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 1, 0]]
    """
    array = np.zeros((len(events), len(slots)), dtype=np.int8)
    for item in solution:
        array[item[0], item[1]] = 1
    return array


def solution_to_schedule(solution, events, slots):
    """Convert a schedule from solution to schedule form

    Parameters
    ----------
    solution : list or tuple
        of tuples of event index and slot index for each scheduled item
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances

    Returns
    -------
    list
        A list of instances of :py:class:`resources.ScheduledItem`
    """
    return [
        ScheduledItem(
            event=events[item[0]],
            slot=slots[item[1]]
        )
        for item in solution
    ]


def schedule_to_array(schedule, events, slots):
    """Convert a schedule from schedule to array form

    Parameters
    ----------
    schedule : list or tuple
        of instances of :py:class:`resources.ScheduledItem`
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances

    Returns
    -------
    np.array
        An E by S array (X) where E is the number of events and S the
        number of slots. Xij is 1 if event i is scheduled in slot j and
        zero otherwise
    """
    array = np.zeros((len(events), len(slots)), dtype=np.int8)
    for item in schedule:
        array[events.index(item.event), slots.index(item.slot)] = 1
    return array


def array_to_schedule(array, events, slots):
    """Convert a schedule from array to schedule form

    Parameters
    ----------
    array : np.array
        An E by S array (X) where E is the number of events and S the
        number of slots. Xij is 1 if event i is scheduled in slot j and
        zero otherwise
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances

    Returns
    -------
    list
        A list of instances of :py:class:`resources.ScheduledItem`
    """
    scheduled = np.transpose(np.nonzero(array))
    return [
        ScheduledItem(event=events[item[0]], slot=slots[item[1]])
        for item in scheduled
    ]


# Functions to compute the difference between two schedules


def event_schedule_difference(old_schedule, new_schedule):
    """Compute the difference between two schedules from an event perspective


    Parameters
    ----------
    old_schedule : list or tuple
        of :py:class:`resources.ScheduledItem` objects
    new_schedule : list or tuple
        of :py:class:`resources.ScheduledItem` objects

    Returns
    -------
    list
        A list of :py:class:`resources.ChangedEventScheduledItem` objects

    Example
    -------

    >>> from conference_scheduler.resources import Event, Slot, ScheduledItem
    >>> from conference_scheduler.scheduler import event_schedule_difference
    >>> events = [Event(f'event_{i}', 30, 0) for i in range(5)]
    >>> slots = [Slot(f'venue_{i}', '', 30, 100, None) for i in range(5)]
    >>> old_schedule = (
    ...     ScheduledItem(events[0], slots[0]),
    ...     ScheduledItem(events[1], slots[1]),
    ...     ScheduledItem(events[2], slots[2]))
    >>> new_schedule = (
    ...     ScheduledItem(events[0], slots[0]),
    ...     ScheduledItem(events[1], slots[2]),
    ...     ScheduledItem(events[2], slots[3]),
    ...     ScheduledItem(events[3], slots[4]))
    >>> diff = (event_schedule_difference(old_schedule, new_schedule))
    >>> print([item.event.name for item in diff])
    ['event_1', 'event_2', 'event_3']
    """
    old = {item.event.name: item for item in old_schedule}
    new = {item.event.name: item for item in new_schedule}

    common_events = set(old.keys()).intersection(new.keys())
    added_events = new.keys() - old.keys()
    removed_events = old.keys() - new.keys()

    changed = [
        ChangedEventScheduledItem(
            old[event].event, old[event].slot, new[event].slot)
        for event in common_events
        if old[event].slot != new[event].slot
    ]
    added = [
        ChangedEventScheduledItem(new[event].event, None, new[event].slot)
        for event in added_events
    ]
    removed = [
        ChangedEventScheduledItem(old[event].event, old[event].slot, None)
        for event in removed_events
    ]
    return sorted(changed + added + removed, key=lambda item: item.event.name)


def slot_schedule_difference(old_schedule, new_schedule):
    """Compute the difference between two schedules from a slot perspective

    Parameters
    ----------
    old_schedule : list or tuple
        of :py:class:`resources.ScheduledItem` objects
    new_schedule : list or tuple
        of :py:class:`resources.ScheduledItem` objects

    Returns
    -------
    list
        A list of :py:class:`resources.ChangedSlotScheduledItem` objects

    Example
    -------

    >>> from conference_scheduler.resources import Event, Slot, ScheduledItem
    >>> from conference_scheduler.scheduler import slot_schedule_difference
    >>> events = [Event(f'event_{i}', 30, 0) for i in range(5)]
    >>> slots = [Slot(f'venue_{i}', '', 30, 100, None) for i in range(5)]
    >>> old_schedule = (
    ...     ScheduledItem(events[0], slots[0]),
    ...     ScheduledItem(events[1], slots[1]),
    ...     ScheduledItem(events[2], slots[2]))
    >>> new_schedule = (
    ...     ScheduledItem(events[0], slots[0]),
    ...     ScheduledItem(events[1], slots[2]),
    ...     ScheduledItem(events[2], slots[3]),
    ...     ScheduledItem(events[3], slots[4]))
    >>> diff = slot_schedule_difference(old_schedule, new_schedule)
    >>> print([item.slot.venue for item in diff])
    ['venue_1', 'venue_2', 'venue_3', 'venue_4']
    """
    old = {item.slot: item for item in old_schedule}
    new = {item.slot: item for item in new_schedule}

    common_slots = set(old.keys()).intersection(new.keys())
    added_slots = new.keys() - old.keys()
    removed_slots = old.keys() - new.keys()

    changed = [
        ChangedSlotScheduledItem(
            old[slot].slot, old[slot].event, new[slot].event)
        for slot in common_slots
        if old[slot].event != new[slot].event
    ]
    added = [
        ChangedSlotScheduledItem(new[slot].slot, None, new[slot].event)
        for slot in added_slots
    ]
    removed = [
        ChangedSlotScheduledItem(old[slot].slot, old[slot].event, None)
        for slot in removed_slots
    ]
    return sorted(
        changed + added + removed,
        key=lambda item: (item.slot.venue, item.slot.starts_at)
    )
