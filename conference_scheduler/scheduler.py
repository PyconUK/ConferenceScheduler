import pulp
import numpy as np
import conference_scheduler.lp_problem as lp
from conference_scheduler.resources import ScheduledItem, Shape


def _all_constraints(events, slots, sessions, X, constraints=None):

    session_array = lp.utils.session_array(sessions)
    tag_array = lp.utils.tag_array(events)
    slot_availability_array = lp.utils.slot_availability_array(events, slots)
    event_availability_array = lp.utils.event_availability_array(events)

    generators = [lp.constraints.all_constraints(
        events, slots, session_array, tag_array, slot_availability_array,
        event_availability_array, X
    )]
    if constraints is not None:
        generators.append(constraints)
    for generator in generators:
        for constraint in generator:
            yield constraint


def constraint_violations(
    events, slots, sessions, array, constraints=None
):
    return (
        c.label
        for c in _all_constraints(
            events, slots, sessions, array, constraints)
        if not c.condition
    )


def is_valid_array(
    events, slots, sessions, array, constraints=None
):
    if len(array) == 0:
        return False
    violations = sum(1 for c in (constraint_violations(
        events, slots, sessions, array, constraints)))
    return violations == 0


def _schedule_to_array(schedule, events, slots):
    array = np.zeros((len(events), len(slots)))
    for item in schedule:
        array[events.index(item.event), slots.index(item.slot)] = 1
    return array


def _array_to_schedule(array, events, slots):
    scheduled = np.transpose(np.nonzero(array))
    return (
        ScheduledItem(event=events[item[0]], slot=slots[item[1]])
        for item in scheduled
    )


def is_valid_schedule(
    schedule, events, slots, sessions, constraints=None
):
    if len(schedule) == 0:
        return False
    array = _schedule_to_array(schedule, events, slots)
    return is_valid_array(events, slots, sessions, array)


def schedule_violations(schedule, events, slots, sessions, constraints=None):
    array = _schedule_to_array(schedule, events, slots)
    return constraint_violations(
        events, slots, sessions, array, constraints)


# Three functions that can be called by external programs to produce the
# schedule in one of three forms:
#   solution: a generator for a list of tuples of event index and slot index
#             for each scheduled item
#   array: a numpy array with rows for events and columns for slots
#   schedule: a generator for a list of ScheduledItem instances


def solution(
    events, slots, sessions, constraints=None, objective_function=None
):
    shape = Shape(len(events), len(slots))
    problem = pulp.LpProblem()
    X = lp.utils.variables(shape)

    for constraint in _all_constraints(
        events, slots, sessions, X, constraints
    ):
        problem += constraint.condition

    if objective_function is not None:
        problem += objective_function(events=events, slots=slots,
                                      sessions=sessions, X=X)

    status = problem.solve()
    if status == 1:
        return (
            item for item, variable in X.items()
            if variable.value() > 0
        )
    else:
        raise ValueError('No valid solution found')


def array(events, slots, sessions, constraints=None, objective_function=None):
    array = np.zeros((len(events), len(slots)))
    for item in solution(
        events, slots, sessions, constraints, objective_function
    ):
        array[item[0], item[1]] = 1
    return array


def schedule(
    events, slots, sessions, constraints=None, objective_function=None
):
    return (
        ScheduledItem(
            event=events[item[0]],
            slot=slots[item[1]]
        )
        for item in solution(
            events, slots, sessions, constraints, objective_function
        )
    )
