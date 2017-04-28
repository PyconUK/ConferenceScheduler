from typing import Sequence
import pulp


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
        mapping a tuple of event index, room index and slot index to an
        instance of pulp.LpVariable.
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


def _max_one_event_per_room_per_slot(variables, events, rooms, slots):
    # A room may not have more than one event scheduled in any slot
    return [
        sum(
            variables[(event_idx, room_idx, slot_idx)]
            for event_idx, event in enumerate(events)
        ) <= 1
        for room_idx, room in enumerate(rooms)
        for slot_idx, slot in enumerate(slots)
    ]


def _only_once_per_event(variables, events, rooms, slots):
    # Each event should be scheduled once and once only
    return [
        sum(
            variables[(event_idx, room_idx, slot_idx)]
            for room_idx, room in enumerate(rooms)
            for slot_idx, slot in enumerate(slots)
        ) == 1
        for event_idx, event in enumerate(events)
    ]


def constraints(variables, events, rooms, slots):
    constraints = []
    constraints.extend(
        _max_one_event_per_room_per_slot(variables, events, rooms, slots)
    )
    constraints.extend(_only_once_per_event(variables, events, rooms, slots))

    return constraints
