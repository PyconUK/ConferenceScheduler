import pulp
from conference_scheduler import scheduler


def test_is_valid_schedule():
    # Test empty schedule
    schedule = tuple()
    problem = pulp.LpProblem()
    assert not scheduler.is_valid_schedule(schedule, problem)


def test_schedule():
    pass
