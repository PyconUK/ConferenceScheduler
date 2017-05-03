import pulp
import itertools as it
import numpy as np
import datetime
from conference_scheduler.resources import Shape, Constraint


def variables(shape: Shape):
    return pulp.LpVariable.dicts(
        "x",
        it.product(range(shape.events), range(shape.slots)),
        cat=pulp.LpBinary
    )


def tag_array(events):
    """
    Return a numpy array mapping events to tags

    - Rows corresponds to events
    - Columns correspond to tags
    """
    all_tags = sorted(set(tag for event in events for tag in event.tags))
    array = np.zeros((len(events), len(all_tags)))
    for row, event in enumerate(events):
        for tag in event.tags:
            array[row, all_tags.index(tag)] = 1
    return array


def session_array(sessions):
    """
    Return a numpy array mapping sessions to slots

    - Rows corresponds to sessions
    - Columns correspond to slots
    """
    # Flatten the list: this assumes that the sessions do not share slots
    all_slots = [slot for session in sessions for slot in session.slots]
    array = np.zeros((len(sessions), len(all_slots)))
    for row, session in enumerate(sessions):
        for slot in session.slots:
            array[row, all_slots.index(slot)] = 1
    return array


def slot_availability_array(events, slots):
    """
    Return a numpy array mapping events to slots

    - Rows corresponds to events
    - Columns correspond to stags

    Array has value 0 if event cannot be scheduled in a given slot
    (1 otherwise)
    """
    array = np.ones((len(events), len(slots)))
    for row, event in enumerate(events):
        for col, slot in enumerate(slots):
            if slot in event.unavailability:
                array[row, col] = 0
    return array


def event_availability_array(events):
    """
    Return a numpy array mapping events to events

    - Rows corresponds to events
    - Columns correspond to events

    Array has value 0 if event cannot be scheduled at same time as other event
    (1 otherwise)
    """
    array = np.ones((len(events), len(events)))
    for row, event in enumerate(events):
        for col, other_event in enumerate(events):
            if other_event in event.unavailability:
                array[row, col] = 0
                array[col, row] = 0
    return array


def start_and_end_dates(slot):
    """
    Return the start and end date of a time slot
    """
    startdate = datetime.datetime.strptime(slot.starts_at, '%d-%b-%Y %H:%M')
    enddate = startdate + datetime.timedelta(minutes=slot.duration)
    return startdate, enddate


def slots_overlap(slot, other_slot):
    """
    Return boolean: whether or not two events overlap
    """
    startdate, enddate = start_and_end_dates(slot)
    other_startdate, other_enddate = start_and_end_dates(other_slot)
    if startdate >= other_startdate and enddate <= other_enddate:
        return True
    if other_startdate >= startdate and other_enddate <= enddate:
        return True
    return False


def concurrent_slots(slots):
    """
    Yields all concurrent slot indices.
    """
    for i, slot in enumerate(slots):
        for j, other_slot in enumerate(slots[i + 1:]):
            if slots_overlap(slot, other_slot):
                yield (i, j + i + 1)


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


def _slots_in_session(slot, session_array):
    """
    Return the indices of the slots in the same session as slot
    """
    return np.nonzero(session_array[slot])[0]


def _events_with_diff_tag(talk, tag_array):
    """
    Return the indices of the events with no tag in common as tag
    """
    event_categories = np.nonzero(tag_array[talk])[0]
    return np.nonzero(sum(tag_array.transpose()[event_categories]) == 0)[0]


def _events_in_session_share_a_tag(session_array, tag_array, X):
    """
    Constraint that ensures that if an event is in a given session then it must
    share at least one tag with all other event in that session.
    """
    label = 'Dissimilar events schedule in same session'
    event_indices = range(len(tag_array))
    session_indices = range(len(session_array))
    for session in session_indices:
        slots = _slots_in_session(session, session_array)
        for slot, event in it.product(slots, event_indices):
            other_events = _events_with_diff_tag(event, tag_array)
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
    label = 'Event clashes with other event'
    for slot1, slot2 in concurrent_slots(slots):
        for row, event in enumerate(event_availability_array):
            for col, availability in enumerate(event):
                yield Constraint(
                    f'{label} - event: {row} and event: {col}',
                    X[row, slot1] + X[col, slot2] <= 1 + availability
                )


def constraints(
    shape, slots, session_array, tag_array, slot_availability_array,
    event_availability_array, X
):
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
