from conference_scheduler import parameters

expected_variables = {}


def test_variables(events, rooms, slots):
    variables = parameters.variables(events, rooms, slots)
    assert variables == expected_variables
