import numpy as np
from conference_scheduler import converter


def test_solution_to_array(valid_solution, valid_array, events, slots):
    array = converter.solution_to_array(valid_solution, events, slots)
    assert np.array_equal(array, valid_array)
    assert all([isinstance(x, np.int8) for x in array.flat])


def test_solution_to_schedule(valid_solution, valid_schedule, events, slots):
    schedule = converter.solution_to_schedule(valid_solution, events, slots)
    assert type(schedule) is list
    assert list(schedule) == valid_schedule


def test_schedule_to_array(valid_schedule, valid_array, events, slots):
    array = converter.schedule_to_array(valid_schedule, events, slots)
    assert np.array_equal(array, valid_array)
    assert all([isinstance(x, np.int8) for x in array.flat])


def test_array_to_schedule(valid_schedule, valid_array, events, slots):
    schedule = list(
        converter.array_to_schedule(valid_array, events, slots)
    )
    assert type(schedule) is list
    assert schedule == valid_schedule
