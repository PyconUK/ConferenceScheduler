from conference_scheduler import parameters


def test_variables(events, rooms, slots):
    variables = parameters.variables(events, rooms, slots)
    assert len(variables) == 24
