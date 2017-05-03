import numpy as np
from conference_scheduler.lp_problem import constraints as lpc


def test_schedule_all_events(shape, X):
    constraints = [
        c.condition for c in lpc._schedule_all_events(shape, X)]
    assert len(constraints) == 3


def test_schedule_all_events_fails_np(shape):
    # Third talk is not scheduled
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._schedule_all_events(shape, X)]
    assert not all(constraints)


def test_schedule_all_events_pass_np(shape):
    # All talks are scheduled
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._schedule_all_events(shape, X)]
    assert all(constraints)


def test_max_one_event_per_slot(shape, X):
    constraints = [
        c.condition for c in lpc._max_one_event_per_slot(shape, X)]
    assert len(constraints) == 7


def test_max_one_events_per_slot_fail_np(shape):
    # Two talks are scheduled in the first slot
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._max_one_event_per_slot(shape, X)]
    assert not all(constraints)


def test_max_one_events_per_slot_pass_np(shape):
    # All slots have at most one talk
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._max_one_event_per_slot(shape, X)]
    assert all(constraints)


def test_events_in_session_share_a_tag(session_array, tag_array, X):
    constraints = [c for c in lpc._events_in_session_share_a_tag(
        session_array, tag_array, X)]
    assert len(constraints) == 16


def test_events_in_session_share_a_tag_fails_np(session_array, tag_array):
    # An array where two talks are in same session but share no tag
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._events_in_session_share_a_tag(
            session_array, tag_array, X)]
    assert not all(constraints)


def test_events_in_session_share_a_tag_passes_np(session_array, tag_array):
    # An array where no two talks are in same session if they do not share tags
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0]
    ])
    test = all(lpc._events_in_session_share_a_tag(
        session_array, tag_array, X))
    assert test is True


def test_events_available_in_scheduled_slot(slot_availability_array, X):
    constraints = [
        c for c in lpc._events_available_in_scheduled_slot(
            slot_availability_array, X)]
    assert len(constraints) == 21


def test_events_available_in_scheduled_slot_fails_np(slot_availability_array):
    # First event is scheduled in a slot for which it is unavailable
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._events_available_in_scheduled_slot(
            slot_availability_array, X)]
    assert all(constraints) is False


def test_events_available_in_scheduled_slot_passes_np(slot_availability_array):
    # All events scheduled in available slots
    X = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition
        for c in lpc._events_available_in_scheduled_slot(
            slot_availability_array, X)]
    assert all(constraints) is True


def test_events_available_during_other_events(
    event_availability_array, slots, X
):
    constraints = [
        c for c in lpc._events_available_during_other_events(
            event_availability_array, slots, X)]
    assert len(constraints) == 45


def test_events_available_during_other_events_fails_np(
    event_availability_array, slots
):
    # First event is scheduled during second event
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._events_available_during_other_events(
            event_availability_array, slots, X)]
    assert all(constraints) is False


def test_events_available_during_other_events_pass_np(
    event_availability_array, slots
):
    # First event is scheduled during second event
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._events_available_during_other_events(
            event_availability_array, slots, X)]
    assert all(constraints) is True


def test_constraints(
    events, slots, session_array, tag_array, slot_availability_array,
    event_availability_array, X
):
    constraints = [
        c for c in lpc.constraints(
            events, slots, session_array, tag_array, slot_availability_array,
            event_availability_array, X)]
    assert len(constraints) == 92
