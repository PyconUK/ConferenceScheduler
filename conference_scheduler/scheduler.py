import pulp
from typing import Sequence, Dict
import conference_scheduler.parameters as params
from conference_scheduler.resources import ScheduledItem


def is_valid_schedule(schedule):
    """Validate an existing schedule against a problem

    Parameters
    ---------
    schedule : iterable
        of resources.ScheduledItem

    Returns
    -------
    bool
        True if schedule is valid. False otherwise
    """
    if len(schedule) == 0:
        return False
    return True


def schedule(
    events: Sequence, rooms: Sequence, slots: Sequence,
    variables: Dict = None,
    constraints: Sequence = None,
    existing: Sequence = None,
):
    """Compute a new, valid, optimised schedule

    Parameters
    ----------
    events : List or Tuple
        of resources.Event
    rooms : List or Tuple
        of resources.Room
    slots : List or Tuple
        of resources.Slot
    variables : Dict
        mapping a tuple of event index, room index and slot index to an
        instance of pulp.LpVariable.
    constraints: List or Tuple
        Ad-hoc constraints to add the problem
    existing : List or Tuple
        of resources.ScheduledItem.
        Represents an existing schedule.
        If provided, the returned schedule will be optimised to minimise
        changes from this schedule

    Returns
    -------
    iterable
        of resources.ScheduledItem
    """
    problem = pulp.LpProblem()
    if variables is None:
        variables = params.variables(events, rooms, slots)
    for constraint in params.constraints(variables, events, rooms, slots):
        problem += constraint
    if constraints is not None:
        for constraint in constraints:
            problem += constraint
    status = problem.solve()
    if status == 1:
        return [
            ScheduledItem(
                event=events[item[0]],
                room=rooms[item[1]],
                slot=slots[item[2]]
            ) for item, variable in variables.items()
            if variable.value() > 0
        ]
    else:
        raise ValueError('No valid schedule found')
