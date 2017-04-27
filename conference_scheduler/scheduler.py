def is_valid_schedule(schedule):
    """Validate an existing schedule against a problem

    Parameters
    ---------
    schedule : iterable
        of resources.ScheduledItem

    Returns
    -------
    bool
        True if schedule is valid. False otherwise
    """
    if len(schedule) == 0:
        return False
    return True


def schedule(existing=None):
    """Compute a new, valid, optimised schedule

    Parameters
    ----------
    existing : iterable
        of resources.ScheduledItem.
        Represents an existing schedule.
        If provided, the returned schedule will be optimised to minimise changes


    Returns
    -------
    iterable
        of resources.ScheduledItem
    """
    return tuple()
