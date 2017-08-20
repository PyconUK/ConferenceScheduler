import itertools as it
from conference_scheduler.resources import Shape, Constraint
from conference_scheduler.lp_problem import utils as lpu


def _schedule_all_events(events, slots, X, summation_type=None, **kwargs):

    shape = Shape(len(events), len(slots))
    summation = lpu.summation_functions[summation_type]

    label = 'Event either not scheduled or scheduled multiple times'
    for event in range(shape.events):
        yield Constraint(
            f'{label} - event: {event}',
            summation(X[event, slot] for slot in range(shape.slots)) == 1
        )


def _max_one_event_per_slot(events, slots, X, summation_type=None, **kwargs):

    shape = Shape(len(events), len(slots))
    summation = lpu.summation_functions[summation_type]

    label = 'Slot with multiple events scheduled'
    for slot in range(shape.slots):
        yield Constraint(
            f'{label} - slot: {slot}',
            summation(X[(event, slot)] for event in range(shape.events)) <= 1
        )


def _events_available_in_scheduled_slot(events, slots, X, **kwargs):
    """
    Constraint that ensures that an event is scheduled in slots for which it is
    available
    """
    slot_availability_array = lpu.slot_availability_array(slots=slots,
                                                          events=events)

    label = 'Event scheduled when not available'
    for row, event in enumerate(slot_availability_array):
        for col, availability in enumerate(event):
            if availability == 0:
                yield Constraint(
                    f'{label} - event: {row}, slot: {col}',
                    X[row, col] <= availability
                )


def _events_available_during_other_events(
    events, slots, X, summation_type=None, **kwargs
):
    """
    Constraint that ensures that an event is not scheduled at the same time as
    another event for which it is unavailable. Unavailability of events is
    either because it is explicitly defined or because they share a tag.
    """
    summation = lpu.summation_functions[summation_type]
    event_availability_array = lpu.event_availability_array(events)

    label = 'Event clashes with another event'
    for slot1, slot2 in lpu.concurrent_slots(slots):
        for row, event in enumerate(event_availability_array):
            if events[row].unavailability:
                for col, availability in enumerate(event):
                    if availability == 0:
                        yield Constraint(
                            f'{label} - event: {row} and event: {col}',
                            summation(
                                (X[row, slot1], X[col, slot2])
                            ) <= 1 + availability
                        )


def _upper_bound_on_event_overflow(
    events, slots, X, beta, summation_type=None, **kwargs
):
    """
    This is an artificial constraint that is used by the objective function
    aiming to minimise the maximum overflow in a slot.
    """
    label = 'Artificial upper bound constraint'
    for row, event in enumerate(events):
        for col, slot in enumerate(slots):
            yield Constraint(
                f'{label} - slot: {col} and event: {row}',
                event.demand * X[row, col] - slot.capacity <= beta)


def all_constraints(events, slots, X, beta=None, summation_type=None):
    kwargs = {
        'events': events,
        'slots': slots,
        'X': X,
        'beta': beta,
        'summation_type': summation_type
    }
    generators = [
        _schedule_all_events,
        _max_one_event_per_slot,
        _events_available_in_scheduled_slot,
        _events_available_during_other_events,
    ]

    if beta is not None:
        generators.append(_upper_bound_on_event_overflow)

    for generator in generators:
        for constraint in generator(**kwargs):
            yield constraint
