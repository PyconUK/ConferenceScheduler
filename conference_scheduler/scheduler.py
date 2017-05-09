import pulp
import numpy as np
import conference_scheduler.lp_problem as lp
from conference_scheduler.resources import (
    ScheduledItem, Shape, ChangedEventScheduledItem, ChangedSlotScheduledItem
)


# Three functions that can be called by external programs to produce the
# schedule in one of three forms:
#   solution: a generator for a list of tuples of event index and slot index
#             for each scheduled item
#   array: a numpy array with rows for events and columns for slots
#   schedule: a generator for a list of ScheduledItem instances


def solution(events, slots, objective_function=None, solver=None, **kwargs):
    """Setup up the ILP problem, submit it to pulp and return the solution

    Parameters
    ----------
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances
        solve : pulp.solver
            a pulp solver
        objective_function: callable
            from lp_problem.objective_functions
        kwargs : keyword arguments
            arguments for the objective function

    Returns
    -------
        Generator
            of tuples giving the event and slot index (for the given events and
            slots lists) for all scheduled items.

            e.g. for a solution where:
                event 0 is scheduled in slot 1
                event 1 is scheduled in slot 4
                event 2 is scheduled in slot 5

            the resulting generator would produce:
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


def array(events, slots, objective_function=None):
    """Compute the ILP solution and return it in array form

     Parameters
    ----------
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances
        objective_function : callable
            from lp_problem.objective_functions

    Returns
    -------
        np.array
            an E by S array (X) where E is the number of events and S the
            number of slots.
            Xij is 1 if event i is scheduled in slot j and zero otherwise

            e.g. 3 events, 7 slots and a solution where:
                event 0 is scheduled in slot 1
                event 1 is scheduled in slot 4
                event 2 is scheduled in slot 5

            the resulting array would be:
                [[0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 1, 0]]
    """
    return solution_to_array(
        solution(events, slots, objective_function),
        events, slots
    )


def schedule(events, slots, objective_function=None, solver=None, **kwargs):
    """Compute the ILP solution and return it in schedule form

     Parameters
    ----------
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances
        solver : pulp.solver
            a pulp solver
        objective_function : callable
            from lp_problem.objective_functions
        kwargs : keyword arguments
            arguments for the objective function

    Returns
    -------
        Generator
            of tuples of instances of resources.ScheduledItem
    """
    return solution_to_schedule(
        solution(events, slots, objective_function, solver=solver, **kwargs),
        events, slots
    )


# Functions to convert the schedule from one form to another

def solution_to_array(solution, events, slots):
    array = np.zeros((len(events), len(slots)))
    for item in solution:
        array[item[0], item[1]] = 1
    return array


def solution_to_schedule(solution, events, slots):
    return [
        ScheduledItem(
            event=events[item[0]],
            slot=slots[item[1]]
        )
        for item in solution
    ]


def schedule_to_array(schedule, events, slots):
    array = np.zeros((len(events), len(slots)))
    for item in schedule:
        array[events.index(item.event), slots.index(item.slot)] = 1
    return array


def array_to_schedule(array, events, slots):
    scheduled = np.transpose(np.nonzero(array))
    return [
        ScheduledItem(event=events[item[0]], slot=slots[item[1]])
        for item in scheduled
    ]


# Functions to compute the difference between two schedules


def event_schedule_difference(old_schedule, new_schedule):
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
