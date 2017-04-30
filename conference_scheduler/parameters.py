from typing import NamedTuple, Sequence
import itertools
import pulp


class Shape(NamedTuple):
    events: int
    rooms: int
    slots: int


def variables(shape):
    """Defines the required instances of pulp.LpVariable

    Parameters
    ----------
    shape

    Returns
    -------
    dict
        mapping a tuple of event index, room index and slot index to an
        instance of pulp.LpVariable.
    """
    return pulp.LpVariable.dicts(
        "x",
        itertools.product(
            range(shape.events), range(shape.rooms), range(shape.slots)
        ),
        cat=pulp.LpBinary
    )


def _max_one_event_per_room_per_slot(variables, shape):
    # A room may only have a maximum of one event scheduled in any time slot
    return [
        sum(
            variables[(event_idx, room_idx, slot_idx)]
            for event_idx in range(shape.events)
        ) <= 1
        for room_idx in range(shape.rooms)
        for slot_idx in range(shape.slots)
    ]


def _only_once_per_event(variables, shape):
    # An event may only be scheduled in one combination of room and time slot
    return [
        sum(
            variables[(event_idx, room_idx, slot_idx)]
            for room_idx in range(shape.rooms)
            for slot_idx in range(shape.slots)
        ) == 1
        for event_idx in range(shape.events)
    ]


def _is_suitable_room(event, room):
    return event.event_type in room.suitability


def _room_suitability(variables, shape, events, rooms):
    # A room may only be scheduled to host an event for which it is deemed
    # suitable
    return [
        sum(
            variables[(events.index(event), rooms.index(room), slot_idx)]
            for slot_idx in range(shape.slots)
        ) == 0
        for room in rooms for event in events
        if not _is_suitable_room(event, room)
    ]


def constraints(variables, events, rooms, slots):
    shape = Shape(len(events), len(rooms), len(slots))
    constraints = []
    constraints.extend(_max_one_event_per_room_per_slot(variables, shape))
    constraints.extend(_only_once_per_event(variables, shape))
    constraints.extend(_room_suitability(variables, shape, events, rooms))

    return constraints
