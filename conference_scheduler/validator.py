from conference_scheduler import scheduler
from conference_scheduler.lp_problem import constraints


def array_violations(array, events, slots):
    """Take a schedule in array form and return any violated constraints

    Parameters
    ----------
        array : np.array
            a schedule in array form
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances
        constraints : list or tuple
            of generator functions which each produce instances of
            resources.Constraint

    Returns
    -------
        Generator
            of a list of strings indicating the nature of the violated
            constraints
    """
    return (
        c.label
        for c in constraints.all_constraints(events, slots, array)
        if not c.condition
    )


def is_valid_array(array, events, slots):
    """Take a schedule in array form and return whether it is a valid
    solution for the given constraints

    Parameters
    ----------
        array : np.array
            a schedule in array form
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances

    Returns
    -------
        bool
            True if array represents a valid solution
    """

    if len(array) == 0:
        return False
    violations = sum(1 for c in (array_violations(array, events, slots)))
    return violations == 0


def is_valid_solution(solution, events, slots):
    """Take a solution and return whether it is valid for the
    given constraints

    Parameters
    ----------
        solution: list or tuple
            a schedule in solution form
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances

    Returns
    -------
        bool
            True if schedule is a valid solution
    """
    if len(solution) == 0:
        return False
    array = scheduler.solution_to_array(solution, events, slots)
    return is_valid_array(array, events, slots)


def solution_violations(solution, events, slots):
    """Take a solution and return a list of violated constraints

    Parameters
    ----------
        solution: list or tuple
            a schedule in solution form
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances

    Returns
    -------
        Generator
            of a list of strings indicating the nature of the violated
            constraints
    """
    array = scheduler.solution_to_array(solution, events, slots)
    return array_violations(array, events, slots)


def is_valid_schedule(schedule, events, slots):
    """Take a schedule and return whether it is a valid solution for the
    given constraints

    Parameters
    ----------
        schedule : list or tuple
            a schedule in schedule form
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances

    Returns
    -------
        bool
            True if schedule is a valid solution
    """
    if len(schedule) == 0:
        return False
    array = scheduler.schedule_to_array(schedule, events, slots)
    return is_valid_array(array, events, slots)


def schedule_violations(schedule, events, slots):
    """Take a schedule and return a list of violated constraints

    Parameters
    ----------
        schedule : list or tuple
            a schedule in schedule form
        events : list or tuple
            of resources.Event instances
        slots : list or tuple
            of resources.Slot instances

    Returns
    -------
        Generator
            of a list of strings indicating the nature of the violated
            constraints
    """
    array = scheduler.schedule_to_array(schedule, events, slots)
    return array_violations(array, events, slots)
