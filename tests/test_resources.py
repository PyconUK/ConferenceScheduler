from conference_scheduler.resources import Event


def test_can_construct_event():
    e = Event(
        name='example',
        duration=60,
        demand=100,
        tags=['beginner', 'python'],
        unavailability=[]
    )
    assert isinstance(e, Event)
    assert e.name == 'example'
    assert e.tags == ['beginner', 'python']
    assert e.unavailability == ()


def test_optional_args_to_event_are_defaulted():
    e = Event(name='example', duration=60, demand=100)
    assert e.tags == []
    assert e.unavailability == ()


def test_optional_args_are_safely_mutable():
    # Construct an instance of `Event` with the optional arguments,
    # omitted, then assign it a tag
    e = Event(name='example', duration=60, demand=100)
    assert e.tags == []
    e.tags.append('intermediate')
    assert e.tags == ['intermediate']

    # Now create a second instance of `Event`, and check we haven't
    # polluted the default arguments.
    f = Event(name='another example', duration=30, demand=50)
    assert f.tags == []


def test_event_is_hashable():
    e = Event(name='example', duration=60, demand=100)
    events = set([e])
    assert len(events) == 1
