from typing import NamedTuple, Callable, List, Dict, Sequence
import pulp
from .resources import ScheduledItem


def variables(events: Sequence, rooms: Sequence, slots: Sequence):
    """Defines the required instances of pulp.LpVariable

    Parameters
    ----------

    Returns
    -------
    dict
        mapping an instance of resource.ScheduledItem to an instance of
        pulp.LpVariable
    """
    variables = {
        ScheduledItem(
            event=events.index(event),
            room=rooms.index(room),
            slot=slots.index(slot)
        ): pulp.LpVariable(
            f'{event.name}_{room.name}_slot_{slots.index(slot)}', cat='Binary'
        )
        for event in events for room in rooms for slot in slots
    }
    return variables


class Constraint(NamedTuple):
    function: Callable
    args: List
    kwargs: Dict
    operator: Callable
    value: int
