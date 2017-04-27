from conference_scheduler import parameters

expected_variables = {}

def test_variables(people):
    variables = parameters.variables(people)
    assert variables == expected_variables
