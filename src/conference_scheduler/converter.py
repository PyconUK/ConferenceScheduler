"""Convert a schedule between the three possible forms"""
import numpy as np
from conference_scheduler.resources import ScheduledItem


def solution_to_array(solution, events, slots):
    """Convert a schedule from solution to array form

    Parameters
    ----------
    solution : list or tuple
        of tuples of event index and slot index for each scheduled item
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances

    Returns
    -------
    np.array
        An E by S array (X) where E is the number of events and S the
        number of slots. Xij is 1 if event i is scheduled in slot j and
        zero otherwise

    Example
    -------
    For For 3 events, 7 slots and the solution::

        [(0, 1), (1, 4), (2, 5)]

    The resulting array would be::

        [[0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 1, 0]]
    """
    array = np.zeros((len(events), len(slots)), dtype=np.int8)
    for item in solution:
        array[item[0], item[1]] = 1
    return array


def solution_to_schedule(solution, events, slots):
    """Convert a schedule from solution to schedule form

    Parameters
    ----------
    solution : list or tuple
        of tuples of event index and slot index for each scheduled item
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances

    Returns
    -------
    list
        A list of instances of :py:class:`resources.ScheduledItem`
    """
    return [
        ScheduledItem(
            event=events[item[0]],
            slot=slots[item[1]]
        )
        for item in solution
    ]


def schedule_to_array(schedule, events, slots):
    """Convert a schedule from schedule to array form

    Parameters
    ----------
    schedule : list or tuple
        of instances of :py:class:`resources.ScheduledItem`
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances

    Returns
    -------
    np.array
        An E by S array (X) where E is the number of events and S the
        number of slots. Xij is 1 if event i is scheduled in slot j and
        zero otherwise
    """
    array = np.zeros((len(events), len(slots)), dtype=np.int8)
    for item in schedule:
        array[events.index(item.event), slots.index(item.slot)] = 1
    return array


def array_to_schedule(array, events, slots):
    """Convert a schedule from array to schedule form

    Parameters
    ----------
    array : np.array
        An E by S array (X) where E is the number of events and S the
        number of slots. Xij is 1 if event i is scheduled in slot j and
        zero otherwise
    events : list or tuple
        of :py:class:`resources.Event` instances
    slots : list or tuple
        of :py:class:`resources.Slot` instances

    Returns
    -------
    list
        A list of instances of :py:class:`resources.ScheduledItem`
    """
    scheduled = np.transpose(np.nonzero(array))
    return [
        ScheduledItem(event=events[item[0]], slot=slots[item[1]])
        for item in scheduled
    ]
