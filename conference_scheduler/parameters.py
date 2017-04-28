from typing import NamedTuple, Callable, List, Dict, Sequence
import pulp
from .resources import ScheduledItem


def variables(events: Sequence, rooms: Sequence, slots: Sequence):
    """Defines the required instances of pulp.LpVariable

    Parameters
    ----------
    events : List or Tuple
        of resources.Event
    rooms : List or Tuple
        of resources.Room
    slots : List or Tuple
        of resources.Slot

    Returns
    -------
    dict
        mapping an instance of resource.ScheduledItem to an instance of
        pulp.LpVariable
    """
    variables = {
        (events.index(event), rooms.index(room), slots.index(slot)):
            pulp.LpVariable(
                f'{event.name}_{room.name}_slot_{slots.index(slot)}',
                cat='Binary'
            )
        for event in events for room in rooms for slot in slots
    }
    return variables


def constraints(variables, events, rooms, slots):
    constraints = []

    # Each event should be scheduled once and once only
    for event in events:
        constraints.append(
            sum(
                variables[(
                    events.index(event),
                    rooms.index(room),
                    slots.index(slot)
                )]
                for room in rooms for slot in slots
            ) == 1
        )

    return constraints


class Constraint(NamedTuple):
    function: Callable
    args: List
    kwargs: Dict
    operator: Callable
    value: int
