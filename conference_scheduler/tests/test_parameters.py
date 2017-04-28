from conference_scheduler import parameters


def test_variables(events, rooms, slots):
    variables = parameters.variables(events, rooms, slots)
    assert len(variables) == 24


def test_max_one_event_per_room_per_slot(variables, events, rooms, slots):
    event_count = len(events)
    room_count = len(rooms)
    slot_count = len(slots)
    constraints = parameters._max_one_event_per_room_per_slot(
        variables, event_count, room_count, slot_count
    )
    # There should be one constraint for each combination of room and slot
    assert len(constraints) == 8


def test_only_once_per_event(variables, events, rooms, slots):
    event_count = len(events)
    room_count = len(rooms)
    slot_count = len(slots)
    constraints = parameters._only_once_per_event(
        variables, event_count, room_count, slot_count
    )
    # There should be one constraint per event
    assert len(constraints) == 3


def test_is_suitable_room(events, rooms):
    assert parameters._is_suitable_room(events[0], rooms[0])
    assert not parameters._is_suitable_room(events[0], rooms[1])


def test_room_suitability(variables, events, rooms, slots):
    slot_count = len(slots)
    constraints = parameters._room_suitability(
        variables, events, rooms, slot_count
    )
    assert len(constraints) == 3


def test_constraints(events, rooms, slots):
    variables = parameters.variables(events, rooms, slots)
    constraints = parameters.constraints(variables, events, rooms, slots)
    assert len(constraints) == 14
