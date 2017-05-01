import pulp
import itertools
import numpy as np
from conference_scheduler.resources import Shape


def variables(shape: Shape):
    return pulp.LpVariable.dicts(
        "x",
        itertools.product(range(shape.events), range(shape.slots)),
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


def _all_talks_in_session_share_a_tag(tags, sessions, X):
    """
    Constraint that ensures that if a talk is in a given session then it must
    share at least one tag with all other talks in that session.
    """


def constraints(shape, X):
    generators = (
        _schedule_all_events,
        _max_one_event_per_slot,
    )
    for generator in generators:
        for constraint in generator(shape, X):
            yield constraint
