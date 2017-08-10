Obtain the mathematical representation of a schedule
====================================================

When scheduling a conference, it might be desirable to recover the schedule in a
different format.
Let us schedule a simple conference as described in :ref:`tutorial`::

    >>> from conference_scheduler.resources import Slot, Event
    >>> from conference_scheduler import scheduler, converter

    >>> slots  = [Slot(venue='Big', starts_at='15-Sep-2016 09:30', duration=30, session="A", capacity=200),
    ...           Slot(venue='Big', starts_at='15-Sep-2016 10:00', duration=30, session="A", capacity=200)]
    >>> events = [Event(name='Talk 1', duration=30, demand=50),
    ...           Event(name='Talk 2', duration=30, demand=130)]

    >>> schedule = scheduler.schedule(events, slots)

We can view this schedule as before::

    >>> for item in schedule:
    ...     print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
    Talk 1 at 15-Sep-2016 09:30 in Big
    Talk 2 at 15-Sep-2016 10:00 in Big

If we want to recover the mathematical array form of our solution (as described
in :ref:`mathematical-model`), we use the :code:`scheduler.schedule_to_array`
function::

    >>> array = converter.schedule_to_array(schedule, events=events, slots=slots)
    >>> array
    array([[1, 0],
           [0, 1]], dtype=int8)

We can also return from a mathematical array to the schedule using the
:code:`scheduler.array_to_schedule` function::

    >>> for item in converter.array_to_schedule(array, events=events, slots=slots):
    ...     print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
    Talk 1 at 15-Sep-2016 09:30 in Big
    Talk 2 at 15-Sep-2016 10:00 in Big
