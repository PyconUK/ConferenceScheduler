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
    solution, events, slots, sessions, constraints=None
):
    return (
        c.label
        for c in _all_constraints(
            events, slots, sessions, solution, constraints)
        if not c.condition
    )


def is_valid_solution(
    solution, events, slots, sessions, constraints=None
):
    if len(solution) == 0:
        return False
    violations = sum(1 for c in (constraint_violations(
        solution, events, slots, sessions, constraints)))
    return violations == 0


def _schedule_to_solution(schedule, events, slots):
    array = np.zeros((len(events), len(slots)))
    for item in schedule:
        array[events.index(item.event), slots.index(item.slot)] = 1
    return array


def _solution_to_schedule(solution, events, slots):
    scheduled = np.transpose(np.nonzero(solution))
    return (
        ScheduledItem(event=events[item[0]], slot=slots[item[1]])
        for item in scheduled
    )


def is_valid_schedule(
    schedule, events, slots, sessions, constraints=None
):
    if len(schedule) == 0:
        return False
    solution = _schedule_to_solution(schedule, events, slots)
    return is_valid_solution(solution, events, slots, sessions)


def schedule_violations(schedule, events, slots, sessions, constraints=None):
    solution = _schedule_to_solution(schedule, events, slots)
    return constraint_violations(
        solution, events, slots, sessions, constraints)


def solution(events, slots, sessions, constraints=None, existing=None,
             objective_function=None):
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


def schedule(events, slots, constraints=None, existing=None):
    shape = Shape(len(events), len(slots))
    return (
        ScheduledItem(
            event=events[item[0]],
            slot=slots[item[1]]
        )
        for item in solution(shape, constraints, existing)
    )
