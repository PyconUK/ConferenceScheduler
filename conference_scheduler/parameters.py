import pulp
import itertools as it
import numpy as np
from conference_scheduler.resources import Shape


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


def _schedule_all_events(shape, X):
    for event in range(shape.events):
        yield sum(X[event, slot] for slot in range(shape.slots)) == 1


def _max_one_event_per_slot(shape, X):
    for slot in range(shape.slots):
        yield sum(X[(event, slot)] for event in range(shape.events)) <= 1


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
    Constraint that ensures that if a talk is in a given session then it must
    share at least one tag with all other talks in that session.
    """
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
                    yield X[(event, slot)] + X[(other_event, other_slot)] <= 1


def constraints(shape, session_array, tag_array, X):
    generators = (
        _schedule_all_events,
        _max_one_event_per_slot,
        _events_in_session_share_a_tag,
    )
    generator_kwargs = (
        {"shape": shape},
        {"shape": shape},
        {"session_array": session_array, "tag_array": tag_array}
    )

    for generator, kwargs in zip(generators, generator_kwargs):
        for constraint in generator(**kwargs, X=X):
            yield constraint
