from conference_scheduler.scheduler import schedule_to_array


def capacity_demand_difference(slots, events, X, **kwargs):
    """
    A function that calculates the difference between demand for an event and
    the slot capacity it is scheduled in.
    """
    overflow = 0
    for row, event in enumerate(events):
        for col, slot in enumerate(slots):
            overflow += (slot.capacity - event.demand) * X[row, col]
    return overflow


def number_of_changes(slots, events, original_schedule, X, **kwargs):
    """
    A function that counts the number of changes between a given schedule
    and an array (either numpy array of lp array).
    """
    changes = 0
    original_array = schedule_to_array(original_schedule, events=events,
                                       slots=slots)
    for row, event in enumerate(original_array):
        for col, slot in enumerate(event):
            if slot == 0:
                changes += X[row, col]
            else:
                changes += 1 - X[row, col]
    return changes
