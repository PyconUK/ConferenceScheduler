Modifying event tags and unavailabiity.
=======================================

As shown in :ref:`tutorial` it is possible to add to the :code:`unavailability`
of an :code:`Event` by using the :code:`Event.add_unavailability` method::

    >>> from conference_scheduler.resources import Slot, Event
    >>> from pprint import pprint

    >>> slots  = [Slot(venue='Big', starts_at='15-Sep-2016 09:30', duration=30, session="A", capacity=200),
    ...           Slot(venue='Big', starts_at='15-Sep-2016 10:00', duration=30, session="A", capacity=200)]
    >>> events = [Event(name='Talk 1', duration=30, demand=50),
    ...           Event(name='Talk 2', duration=30, demand=130)]

Let us note the first event as unavailable for the first slot::

    >>> events[0].add_unavailability(*slots)
    >>> pprint(events[0].unavailability)
    (Slot(venue='Big', starts_at='15-Sep-2016 09:30', duration=30, capacity=200, session='A'),
     Slot(venue='Big', starts_at='15-Sep-2016 10:00', duration=30, capacity=200, session='A'))

We can remove a specific item::

    >>> events[0].remove_unavailability(slots[0])
    >>> events[0].unavailability
    (Slot(venue='Big', starts_at='15-Sep-2016 10:00', duration=30, capacity=200, session='A'),)

We can also completely clear the unavailability::

    >>> events[0].clear_unavailability()
    >>> events[0].unavailability
    ()

Similar methods exist for modifying event :code:`tags`::

    >>> events[0].add_tags('Python', 'Ruby', 'Javascript')
    >>> events[0].tags
    ('Python', 'Ruby', 'Javascript')
    >>> events[0].remove_tag("Python")
    >>> events[0].tags
    ('Ruby', 'Javascript')
    >>> events[0].clear_tags()
    >>> events[0].tags
    ()

