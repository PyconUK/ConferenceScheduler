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
    assert e.tags == ('beginner', 'python')
    assert e.unavailability == ()


def test_optional_args_to_event_are_defaulted():
    e = Event(name='example', duration=60, demand=100)
    assert e.tags == ()
    assert e.unavailability == ()


def test_optional_args_are_safely_mutable():
    # Construct an instance of `Event` with the optional arguments,
    # omitted, then assign it a tag
    e = Event(name='example', duration=60, demand=100)
    assert e.tags == ()
    e.add_tag('intermediate')
    assert e.tags == ('intermediate', )

    # Now create a second instance of `Event`, and check we haven't
    # polluted the default arguments.
    f = Event(name='another example', duration=30, demand=50)
    assert f.tags == ()


def test_event_is_hashable():
    e = Event(name='example', duration=60, demand=100)
    events = set([e])
    assert len(events) == 1


def test_add_unavailability_append():
    e = Event(name='example', duration=60, demand=100)
    e.add_unavailability(2)
    assert e.unavailability == (2, )


def test_add_unavailability_extend():
    e = Event(name='example', duration=60, demand=100)
    e.add_unavailability([2, 3, 4])
    assert e.unavailability == (2, 3, 4)


def test_remove_unavailability():
    e = Event(name='example', duration=60, demand=100)
    e.add_unavailability([2, 3, 4])
    e.remove_unavailability(3)
    assert e.unavailability == (2, 4)


def test_clear_unavailability():
    e = Event(name='example', duration=60, demand=100)
    e.add_unavailability([2, 3, 4])
    e.clear_unavailability()
    assert e.unavailability == ()


def test_add_tag():
    e = Event(name='example', duration=60, demand=100)
    e.add_tag('test')
    assert e.tags == ('test', )


def test_add_tags():
    e = Event(name='example', duration=60, demand=100)
    e.add_tags(['test1', 'test2', 'test3'])
    assert e.tags == ('test1', 'test2', 'test3')


def test_remove_tag():
    e = Event(name='example', duration=60, demand=100)
    e.add_tags(['test1', 'test2', 'test3'])
    e.remove_tag('test2')
    assert e.tags == ('test1', 'test3')


def test_clear_tags():
    e = Event(name='example', duration=60, demand=100)
    e.add_tags(['test1', 'test2', 'test3'])
    e.clear_tags()
    assert e.tags == ()
