import pulp
import itertools as it
import numpy as np
import datetime
from conference_scheduler.resources import Shape


# According to David MacIver, using this function is more efficient than
# using sum() or plain addition
# This code is taken from his gist at:
# https://gist.github.com/DRMacIver/4b6561c8e4776597bf7568ccac52742f
def lpsum(variables):
    result = pulp.LpAffineExpression()
    for v in variables:
        result.addInPlace(v)
    return result


summation_functions = {
    'lpsum': lpsum,
    None: sum
}


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


def session_array(slots):
    """
    Return a numpy array mapping sessions to slots

    - Rows corresponds to sessions
    - Columns correspond to slots
    """
    # Flatten the list: this assumes that the sessions do not share slots
    sessions = sorted(set([slot.session for slot in slots]))
    array = np.zeros((len(sessions), len(slots)))
    for col, slot in enumerate(slots):
        array[sessions.index(slot.session), col] = 1
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
            if slot in event.unavailability or event.duration > slot.duration:
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
