import numpy as np
from conference_scheduler.lp_problem import utils as lpu


def test_tag_array(events):
    tag_array = lpu.tag_array(events)
    assert np.array_equal(tag_array, np.array([[1, 0], [1, 1], [0, 1]]))


def test_session_array(sessions):
    session_array = lpu.session_array(sessions)
    assert np.array_equal(session_array, np.array([
        [1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1]
    ]))


def test_slot_availability_array(events, slots):
    slot_availability_array = lpu.slot_availability_array(events, slots)
    assert np.array_equal(slot_availability_array, np.array([
        [0, 0, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]))


def test_event_availability_array(events):
    event_availability_array = lpu.event_availability_array(events)
    assert np.array_equal(event_availability_array, np.array([
        [1, 0, 1, ],
        [0, 1, 1, ],
        [1, 1, 1, ]
    ]))


def test_slots_overlap(slots):
    assert lpu.slots_overlap(slots[0], slots[1]) is False
    assert lpu.slots_overlap(slots[0], slots[2]) is False
    assert lpu.slots_overlap(slots[0], slots[3]) is False
    assert lpu.slots_overlap(slots[0], slots[4]) is False
    assert lpu.slots_overlap(slots[0], slots[6]) is False
    assert lpu.slots_overlap(slots[1], slots[6]) is False
    assert lpu.slots_overlap(slots[1], slots[4]) is False
    assert lpu.slots_overlap(slots[6], slots[1]) is False
    assert lpu.slots_overlap(slots[1], slots[6]) is False

    assert lpu.slots_overlap(slots[0], slots[0]) is True
    assert lpu.slots_overlap(slots[5], slots[0]) is True
    assert lpu.slots_overlap(slots[0], slots[5]) is True
    assert lpu.slots_overlap(slots[1], slots[5]) is True
    assert lpu.slots_overlap(slots[5], slots[1]) is True
    assert lpu.slots_overlap(slots[6], slots[6]) is True


def test_concurrent_slots(slots):
    slots = list(lpu.concurrent_slots(slots))
    assert slots == [(0, 5), (1, 5), (2, 6), (3, 6), (4, 6)]


def test_variables(shape):
    X = lpu.variables(shape)
    assert len(X) == 21


def test_slots_in_session(session_array):
    assert np.array_equal(lpu._slots_in_session(0, session_array),
                          np.array([0, 1, 2]))
    assert np.array_equal(lpu._slots_in_session(3, session_array),
                          np.array([6]))


def test_events_with_diff_tags(tag_array):
    assert np.array_equal(lpu._events_with_diff_tag(0, tag_array),
                          np.array([2]))
    assert np.array_equal(lpu._events_with_diff_tag(1, tag_array),
                          np.array([]))
    assert np.array_equal(lpu._events_with_diff_tag(2, tag_array),
                          np.array([0]))
