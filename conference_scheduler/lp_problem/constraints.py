import itertools as it
from conference_scheduler.resources import Shape, Constraint
from conference_scheduler.lp_problem import utils as lpu


def _schedule_all_events(shape, X):
    label = 'Event either not scheduled or scheduled multiple times'
    for event in range(shape.events):
        yield Constraint(
            f'{label} - event: {event}',
            sum(X[event, slot] for slot in range(shape.slots)) == 1
        )


def _max_one_event_per_slot(shape, X):
    label = 'Slot with multiple events scheduled'
    for slot in range(shape.slots):
        yield Constraint(
            f'{label} - slot: {slot}',
            sum(X[(event, slot)] for event in range(shape.events)) <= 1
        )


def _events_in_session_share_a_tag(session_array, tag_array, X):
    """
    Constraint that ensures that if an event is in a given session then it must
    share at least one tag with all other event in that session.
    """
    label = 'Dissimilar events schedule in same session'
    event_indices = range(len(tag_array))
    session_indices = range(len(session_array))
    for session in session_indices:
        slots = lpu._slots_in_session(session, session_array)
        for slot, event in it.product(slots, event_indices):
            other_events = lpu._events_with_diff_tag(event, tag_array)
            for other_slot, other_event in it.product(slots, other_events):
                if other_slot != slot and other_event != event:
                    # If they have different tags they cannot be scheduled
                    # together
                    yield Constraint(
                        f'{label} - event: {event}, slot: {slot}',
                        X[(event, slot)] + X[(other_event, other_slot)] <= 1
                    )


def _events_available_in_scheduled_slot(slot_availability_array, X):
    """
    Constraint that ensures that an event is scheduled in slots for which it is
    available
    """
    label = 'Event scheduled when not available'
    for row, event in enumerate(slot_availability_array):
        for col, availability in enumerate(event):
            yield Constraint(
                f'{label} - event: {row}, slot: {col}',
                X[row, col] <= availability
            )


def _events_available_during_other_events(
    event_availability_array, slots, X
):
    """
    Constraint that ensures that an event is not scheduled at the same time as
    another event for which it is unavailable.
    """
    label = 'Event clashes with another event'
    for slot1, slot2 in lpu.concurrent_slots(slots):
        for row, event in enumerate(event_availability_array):
            for col, availability in enumerate(event):
                yield Constraint(
                    f'{label} - event: {row} and event: {col}',
                    X[row, slot1] + X[col, slot2] <= 1 + availability
                )


def all_constraints(
    events, slots, session_array, tag_array, slot_availability_array,
    event_availability_array, X
):
    shape = Shape(len(events), len(slots))
    generators = (
        _schedule_all_events,
        _max_one_event_per_slot,
        _events_in_session_share_a_tag,
        _events_available_in_scheduled_slot,
        _events_available_during_other_events
    )
    generator_kwargs = (
        {"shape": shape},
        {"shape": shape},
        {"session_array": session_array, "tag_array": tag_array},
        {"slot_availability_array": slot_availability_array},
        {"event_availability_array": event_availability_array, 'slots': slots}
    )

    for generator, kwargs in zip(generators, generator_kwargs):
        for constraint in generator(**kwargs, X=X):
            yield constraint
