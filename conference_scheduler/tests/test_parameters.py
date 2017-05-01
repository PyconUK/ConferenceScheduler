from conference_scheduler import parameters
import numpy as np

def test_tags(events):
    tags = parameters.tags(events)
    assert np.array_equal(tags, np.array([[1, 0], [1, 1], [0, 1]]))

def test_variables(shape):
    X = parameters.variables(shape)
    assert len(X) == 21


def test_schedule_all_events(shape, X):
    constraints = [c for c in parameters._schedule_all_events(shape, X)]
    assert len(constraints) == 3


def test_max_one_event_per_slot(shape, X):
    constraints = [c for c in parameters._max_one_event_per_slot(shape, X)]
    assert len(constraints) == 7


def test_all_talks_in_session_share_a_tag(events):
    constraints = list(parameters._all_talks_in_session_share_a_tag(tags, X))
    assert len(constraints) == 7

def test_constraints(shape, X):
    constraints = [c for c in parameters.constraints(shape, X)]
    assert len(constraints) == 10
