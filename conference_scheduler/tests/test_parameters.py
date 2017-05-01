from conference_scheduler import parameters
import numpy as np

def test_tag_array(events):
    tag_array = parameters.tag_array(events)
    assert np.array_equal(tag_array, np.array([[1, 0], [1, 1], [0, 1]]))

def test_session_array(sessions):
    session_array = parameters.session_array(sessions)
    assert np.array_equal(session_array, np.array([[1, 1, 1, 0, 0, 0, 0],
                                                   [0, 0, 0, 1, 1, 0, 0],
                                                   [0, 0, 0, 0, 0, 1, 0],
                                                   [0, 0, 0, 0, 0, 0, 1]]))

def test_variables(shape):
    X = parameters.variables(shape)
    assert len(X) == 21


def test_schedule_all_events(shape, X):
    constraints = [c for c in parameters._schedule_all_events(shape, X)]
    assert len(constraints) == 3

def test_schedule_all_events_fails_np(shape):
    # Third talk is not scheduled
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]])
    constraint = all(parameters._schedule_all_events(shape, X))
    assert constraint is False

def test_schedule_all_events_pass_np(shape):
    # All talks are scheduled
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraint = all(parameters._schedule_all_events(shape, X))
    assert constraint is True


def test_max_one_event_per_slot(shape, X):
    constraints = [c for c in parameters._max_one_event_per_slot(shape, X)]
    assert len(constraints) == 7

def test_max_one_events_per_slot_fail_np(shape):
    # Two talks are scheduled in the first slot
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraint = all(parameters._max_one_event_per_slot(shape, X))
    assert constraint is False

def test_max_one_events_per_slot_pass_np(shape):
    # All slots have at most one talk
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraint = all(parameters._max_one_event_per_slot(shape, X))
    assert constraint is True


def test_talks_in_session_share_a_tag(session_array, tag_array, X):
    constraints = [c for c in
            parameters._talks_in_session_share_a_tag(session_array, tag_array, X)]
    assert len(constraints) == 16

def test_talks_in_session_share_a_tag_fails_np(session_array, tag_array):
    # An array where two talks are in same session but share no tag
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraint = all(parameters._talks_in_session_share_a_tag(session_array,
                                                              tag_array, X))
    assert constraint is False

def test_talks_in_session_share_a_tag_passes_np(session_array, tag_array):
    # An array where no two talks are in same session if they do not share tags
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 1, 0, 0, 0]])
    test = all(parameters._talks_in_session_share_a_tag(session_array,
                                                        tag_array, X))
    assert test is True



def test_constraints(shape, session_array, tag_array, X):
    constraints = [c for c in parameters.constraints(shape, session_array,
                                                     tag_array, X)]
    assert len(constraints) == 26
