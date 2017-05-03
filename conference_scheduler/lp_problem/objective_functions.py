def capacity_demand_difference(slots, events, X, **kwargs):
    """
    A function that minimises the difference between demand for an event and
    the slot capacity it is scheduled in.
    """
    overflow = 0
    for row, event in enumerate(events):
        for col, slot in enumerate(slots):
            overflow += (slot.capacity - event.demand) * X[row, col]
    return overflow
