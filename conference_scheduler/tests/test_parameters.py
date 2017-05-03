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

def test_slot_availability_array(events, slots):
    slot_availability_array = parameters.slot_availability_array(events, slots)
    assert np.array_equal(slot_availability_array, np.array(
        [[0, 0, 1, 1, 1, 1, 1],
         [1, 1, 0, 0, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1]]))

def test_event_availability_array(events):
    event_availability_array = parameters.event_availability_array(events)
    assert np.array_equal(event_availability_array, np.array(
        [[1, 0, 1, ],
         [0, 1, 1, ],
         [1, 1, 1, ]]))

def test_slots_overlap(slots):
    assert parameters.slots_overlap(slots[0], slots[1]) is False
    assert parameters.slots_overlap(slots[0], slots[2]) is False
    assert parameters.slots_overlap(slots[0], slots[3]) is False
    assert parameters.slots_overlap(slots[0], slots[4]) is False
    assert parameters.slots_overlap(slots[0], slots[6]) is False
    assert parameters.slots_overlap(slots[1], slots[6]) is False
    assert parameters.slots_overlap(slots[1], slots[4]) is False
    assert parameters.slots_overlap(slots[6], slots[1]) is False
    assert parameters.slots_overlap(slots[1], slots[6]) is False

    assert parameters.slots_overlap(slots[0], slots[0]) is True
    assert parameters.slots_overlap(slots[5], slots[0]) is True
    assert parameters.slots_overlap(slots[0], slots[5]) is True
    assert parameters.slots_overlap(slots[1], slots[5]) is True
    assert parameters.slots_overlap(slots[5], slots[1]) is True
    assert parameters.slots_overlap(slots[6], slots[6]) is True

def test_concurrent_slots(slots):
    slots = list(parameters.concurrent_slots(slots))
    assert slots == [(0, 5), (1, 5), (2, 6), (3, 6), (4, 6)]

def test_variables(shape):
    X = parameters.variables(shape)
    assert len(X) == 21


def test_schedule_all_events(shape, X):
    constraints = [
        c.condition for c in parameters._schedule_all_events(shape, X)]
    assert len(constraints) == 3


def test_schedule_all_events_fails_np(shape):
    # Third talk is not scheduled
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]])
    constraints = [
        c.condition for c in parameters._schedule_all_events(shape, X)]
    assert not all(constraints)


def test_schedule_all_events_pass_np(shape):
    # All talks are scheduled
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraints = [
        c.condition for c in parameters._schedule_all_events(shape, X)]
    assert all(constraints)


def test_max_one_event_per_slot(shape, X):
    constraints = [
        c.condition for c in parameters._max_one_event_per_slot(shape, X)]
    assert len(constraints) == 7


def test_max_one_events_per_slot_fail_np(shape):
    # Two talks are scheduled in the first slot
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraints = [
        c.condition for c in parameters._max_one_event_per_slot(shape, X)]
    assert not all(constraints)


def test_max_one_events_per_slot_pass_np(shape):
    # All slots have at most one talk
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraints = [
        c.condition for c in parameters._max_one_event_per_slot(shape, X)]
    assert all(constraints)


def test_slots_in_session(session_array):
    assert np.array_equal(parameters._slots_in_session(0, session_array),
                          np.array([0, 1, 2]))
    assert np.array_equal(parameters._slots_in_session(3, session_array),
                          np.array([6]))


def test_events_with_diff_tags(tag_array):
    assert np.array_equal(parameters._events_with_diff_tag(0, tag_array),
                          np.array([2]))
    assert np.array_equal(parameters._events_with_diff_tag(1, tag_array),
                          np.array([]))
    assert np.array_equal(parameters._events_with_diff_tag(2, tag_array),
                          np.array([0]))


def test_events_in_session_share_a_tag(session_array, tag_array, X):
    constraints = [c for c in parameters._events_in_session_share_a_tag(
        session_array, tag_array, X)]
    assert len(constraints) == 16


def test_events_in_session_share_a_tag_fails_np(session_array, tag_array):
    # An array where two talks are in same session but share no tag
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraints = [
        c.condition for c in parameters._events_in_session_share_a_tag(
            session_array, tag_array, X)]
    assert not all(constraints)


def test_events_in_session_share_a_tag_passes_np(session_array, tag_array):
    # An array where no two talks are in same session if they do not share tags
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 1, 0, 0, 0]])
    test = all(parameters._events_in_session_share_a_tag(session_array,
                                                         tag_array, X))
    assert test is True


def test_events_available_in_scheduled_slot(slot_availability_array, X):
    constraints = [c for c in
            parameters._events_available_in_scheduled_slot(
                slot_availability_array, X)]
    assert len(constraints) == 21


def test_events_available_in_scheduled_slot_fails_np(slot_availability_array):
    # First event is scheduled in a slot for which it is unavailable
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraint = all(parameters._events_available_in_scheduled_slot(
        slot_availability_array, X))
    assert constraint is False


def test_events_available_in_scheduled_slot_passes_np(slot_availability_array):
    # All events scheduled in available slots
    X = np.array([[0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraint = all(parameters._events_available_in_scheduled_slot(
        slot_availability_array, X))
    assert constraint is True


def test_events_available_during_other_events(event_availability_array, slots, X):
    constraints = [c for c in
            parameters._events_available_during_other_events(
                event_availability_array, slots, X)]
    assert len(constraints) == 45


def test_events_available_during_other_events_fails_np(event_availability_array,
                                                       slots):
    # First event is scheduled during second event
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraint = all(parameters._events_available_during_other_events(event_availability_array, slots, X))
    assert constraint is False

def test_events_available_during_other_events_pass_np(event_availability_array,
                                                       slots):
    # First event is scheduled during second event
    X = np.array([[1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1],
                  [0, 1, 0, 0, 0, 0, 0]])
    constraint = all(parameters._events_available_during_other_events(event_availability_array, slots, X))
    assert constraint is True


def test_constraints(shape, session_array, tag_array,
                     slot_availability_array, X):
    constraints = [c for c in parameters.constraints(shape,
        session_array, tag_array, slot_availability_array, X)]
    assert len(constraints) == 47
