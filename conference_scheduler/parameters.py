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
    # A room may only have a maximum of one event scheduled in any time slot
    return [
        sum(
            variables[(event_idx, room_idx, slot_idx)]
            for event_idx in range(event_count)
        ) <= 1
        for room_idx in range(room_count)
        for slot_idx in range(slot_count)
    ]


def _only_once_per_event(variables, event_count, room_count, slot_count):
    # An event may only be scheduled in one combination of room and time slot
    return [
        sum(
            variables[(event_idx, room_idx, slot_idx)]
            for room_idx in range(room_count)
            for slot_idx in range(slot_count)
        ) == 1
        for event_idx in range(event_count)
    ]


def _is_suitable_room(event, room):
    return event.event_type in room.suitability


def _room_suitability(variables, events, rooms, slot_count):
    # A room may only be scheduled to host an event for which it is deemed
    # suitable
    return [
        sum(
            variables[(events.index(event), rooms.index(room), slot_idx)]
            for slot_idx in range(slot_count)
        ) == 0
        for room in rooms for event in events
        if not _is_suitable_room(event, room)
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
    constraints.extend(_room_suitability(variables, events, rooms, slot_count))

    return constraints
