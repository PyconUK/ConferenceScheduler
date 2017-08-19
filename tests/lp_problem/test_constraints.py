import pulp
import numpy as np
from conference_scheduler.lp_problem import constraints as lpc


def test_schedule_all_events(events, slots, X):
    constraints = [
        c.condition for c in lpc._schedule_all_events(events, slots, X)]
    assert len(constraints) == 3


def test_schedule_all_events_fails_np(events, slots):
    # Third talk is not scheduled
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._schedule_all_events(events, slots, X)]
    assert not all(constraints)


def test_schedule_all_events_pass_np(events, slots):
    # All talks are scheduled
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._schedule_all_events(events, slots, X)]
    assert all(constraints)


def test_max_one_event_per_slot(events, slots, X):
    constraints = [
        c.condition for c in lpc._max_one_event_per_slot(events, slots, X)]
    assert len(constraints) == 7


def test_max_one_events_per_slot_fail_np(events, slots):
    # Two talks are scheduled in the first slot
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._max_one_event_per_slot(events, slots, X)]
    assert not all(constraints)


def test_max_one_events_per_slot_pass_np(events, slots):
    # All slots have at most one talk
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._max_one_event_per_slot(events, slots, X)]
    assert all(constraints)


def test_events_available_in_scheduled_slot(events, slots, X):
    constraints = [
        c for c in lpc._events_available_in_scheduled_slot(
            events, slots, X)]
    assert len(constraints) == 9


def test_events_available_in_scheduled_slot_fails_np(events, slots):
    # First event is scheduled in a slot for which it is unavailable
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._events_available_in_scheduled_slot(
            events, slots, X)]
    assert all(constraints) is False


def test_events_available_in_scheduled_slot_passes_np(events, slots):
    # All events scheduled in available slots
    X = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    constraints = [
        c.condition
        for c in lpc._events_available_in_scheduled_slot(
            events, slots, X)]
    assert all(constraints) is True


def test_events_available_during_other_events(events, slots, X):
    constraints = [
        c for c in lpc._events_available_during_other_events(events, slots, X)]
    assert len(constraints) == 15


def test_events_available_during_other_events_fails_np(events, slots):
    # First event is scheduled during second event
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._events_available_during_other_events(
            events, slots, X)]
    assert all(constraints) is False


def test_events_available_during_other_events_pass_np(events, slots):
    # First event is scheduled during second event
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._events_available_during_other_events(
            events, slots, X)]
    assert all(constraints) is True


def test_upper_bound_on_event_overflow(events, slots, X):
    constraints = [
        c for c in lpc._upper_bound_on_event_overflow(
            events,
            slots,
            X,
            beta=float('inf'))]
    assert len(constraints) == len(slots) * len(events)


def test_upper_bound_on_event_overflow_np(events, slots):
    # First event is scheduled during second event
    X = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    constraints = [
        c.condition for c in lpc._upper_bound_on_event_overflow(
            events, slots, X, beta=float('inf'))]
    assert all(constraints) is True

    constraints = [
        c.condition for c in lpc._upper_bound_on_event_overflow(
            events, slots, X, beta=200)]
    assert all(constraints) is False


def test_constraints(events, slots, X):
    constraints = [
        c for c in lpc.all_constraints(
            events, slots, X)]
    assert len(constraints) == 34

def test_constraints(events, slots, X):
    beta = pulp.LpVariable("upper_bound")
    constraints = [
        c for c in lpc.all_constraints(
            events, slots, X, beta)]
    assert len(constraints) == 55
