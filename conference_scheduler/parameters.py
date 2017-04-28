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


def _max_one_event_per_room_per_slot(
    variables, event_count, room_count, slot_count
):
    # A room may not have more than one event scheduled in any slot
    return [
        sum(
            variables[(event_idx, room_idx, slot_idx)]
            for event_idx in range(event_count)
        ) <= 1
        for room_idx in range(room_count)
        for slot_idx in range(slot_count)
    ]


def _only_once_per_event(
    variables, event_count, room_count, slot_count
):
    # Each event should be scheduled once and once only
    return [
        sum(
            variables[(event_idx, room_idx, slot_idx)]
            for room_idx in range(room_count)
            for slot_idx in range(slot_count)
        ) == 1
        for event_idx in range(event_count)
    ]


def constraints(variables, events, rooms, slots):
    event_count = len(events)
    room_count = len(rooms)
    slot_count = len(slots)
    constraints = []
    constraints.extend(
        _max_one_event_per_room_per_slot(
            variables, event_count, room_count, slot_count
        )
    )
    constraints.extend(
        _only_once_per_event(
            variables, event_count, room_count, slot_count
        )
    )

    return constraints
