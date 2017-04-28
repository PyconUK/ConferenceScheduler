from conference_scheduler import scheduler


def test_is_valid_schedule(people):
    # Test empty schedule
    schedule = tuple()
    assert not scheduler.is_valid_schedule(schedule)


def test_schedule(events, rooms, slots):
    scheduler.schedule(events, rooms, slots)
