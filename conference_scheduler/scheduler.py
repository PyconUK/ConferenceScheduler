import pulp
import conference_scheduler.parameters as params
from conference_scheduler.resources import ScheduledItem


def _all_constraints(shape, sessions, events, X, constraints=None):
    session_array = params.session_array(sessions)
    tag_array = params.tag_array(events)
    generators = [params.constraints(shape, session_array, tag_array, X)]
    if constraints is not None:
        generators.append(constraints)
    for generator in generators:
        for constraint in generator:
            yield constraint


def constraint_violations(solution, shape, sessions, events, constraints=None):
    return [
        c.label
        for c in _all_constraints(
            shape, sessions, events, solution, constraints)
        if not c.condition
    ]


def is_valid_solution(solution, shape, sessions, events, constraints=None):
    if len(solution) == 0:
        return False
    return all([c.condition for c in _all_constraints(
        shape, sessions, events, solution, constraints)
    ])


def solution(shape, events, sessions, constraints=None, existing=None):
    problem = pulp.LpProblem()
    X = params.variables(shape)

    for constraint in _all_constraints(
        shape, sessions, events, X, constraints
    ):
        problem += constraint.condition
    status = problem.solve()
    if status == 1:
        return (
            item for item, variable in X.items()
            if variable.value() > 0
        )
    else:
        raise ValueError('No valid solution found')


def schedule(events, slots, constraints=None, existing=None):
    shape = params.Shape(len(events), len(slots))
    return (
        ScheduledItem(
            event=events[item[0]],
            slot=slots[item[1]]
        )
        for item in solution(shape, constraints, existing)
    )
