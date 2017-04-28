from conference_scheduler import scheduler


def test_is_valid_schedule(people):
    # Test empty schedule
    schedule = tuple()
    assert not scheduler.is_valid_schedule(schedule)


def test_schedule(events, rooms, slots):
    schedule = scheduler.schedule(events, rooms, slots)

    # Each event should be scheduled once and once only
    assert len(schedule) == len(events)
    scheduled_events = set([item.event.name for item in schedule])
    assert scheduled_events == set([event.name for event in events])
