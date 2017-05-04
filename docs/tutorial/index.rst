Tutorial
========

Welcome! You are the head scheduler for the upcoming :code:`name` con. You have
a venue, you have talks and you have a week to schedule everything!

Your venue has two rooms in which you will schedule talks and workshops in
parallel but you're also going to want to find time for some social events.

You have organised your time slots as follows:

- The first day will have 2 sessions (morning and afternoon) with two 30 minute
  time slots in each room.
- The second day will have 1 room used for longer 1 hour workshops, the other
  room used for more talks and 2 long sessions set aside for the social events.

Let us create these time slots using the :code:`conference_scheduler`::

    >>> from conference_scheduler.resources import Slot, Event

    >>> talk_slots  = [Slot(venue='Big', starts_at='15-Sep-2016 09:30', duration=30, session="A", capacity=200),
    ...                Slot(venue='Big', starts_at='15-Sep-2016 10:00', duration=30, session="A", capacity=200),
    ...                Slot(venue='Small', starts_at='15-Sep-2016 09:30', duration=30, session="B", capacity=50),
    ...                Slot(venue='Small', starts_at='15-Sep-2016 10:00', duration=30, session="B", capacity=50),
    ...                Slot(venue='Big', starts_at='15-Sep-2016 12:30', duration=30, session="C", capacity=200),
    ...                Slot(venue='Big', starts_at='15-Sep-2016 13:00', duration=30, session="C", capacity=200),
    ...                Slot(venue='Small', starts_at='15-Sep-2016 12:30', duration=30, session="D", capacity=50),
    ...                Slot(venue='Small', starts_at='15-Sep-2016 13:00', duration=30, session="D", capacity=50),
    ...                Slot(venue='Big', starts_at='16-Sep-2016 09:30', duration=30, session="E", capacity=50),
    ...                Slot(venue='Big', starts_at='16-Sep-2016 10:00', duration=30, session="E", capacity=50),
    ...                Slot(venue='Big', starts_at='16-Sep-2016 12:30', duration=30, session="F", capacity=50),
    ...                Slot(venue='Big', starts_at='16-Sep-2016 13:00', duration=30, session="F", capacity=50)]
    >>> workshop_slots = [Slot(venue='Small', starts_at='16-Sep-2016 09:30', duration=60, session="G", capacity=50),
    ...                   Slot(venue='Small', starts_at='16-Sep-2016 13:00', duration=60, session="H", capacity=50)]
    >>> outside_slots = [Slot(venue='Outside', starts_at='16-Sep-2016 12:30', duration=90, session="I", capacity=1000),
    ...                  Slot(venue='Outside', starts_at='16-Sep-2016 13:00', duration=90, session="J", capacity=1000)]
    >>> slots = talk_slots + workshop_slots + outside_slots


We also have a number of talks and workshops to schedule, because of the
duration/location of the slots we know some of them are unavailable for a given slot::

    >>> events = [Event(name='Talk 1', event_type='talk', duration=30, roles="empty", tags=['beginner'], unavailability=outside_slots, demand=50),
    ...           Event(name='Talk 2', event_type='talk', duration=30, roles="empty", tags=['beginner'], unavailability=outside_slots, demand=130),
    ...           Event(name='Talk 3', event_type='talk', duration=30, roles="empty", tags=['beginner'], unavailability=outside_slots, demand=500),
    ...           Event(name='Talk 4', event_type='talk', duration=30, roles="empty", tags=['beginner'], unavailability=outside_slots, demand=30),
    ...           Event(name='Talk 5', event_type='talk', duration=30, roles="empty", tags=['intermediate'], unavailability=outside_slots, demand=60),
    ...           Event(name='Talk 6', event_type='talk', duration=30, roles="empty", tags=['intermediate'], unavailability=outside_slots, demand=30),
    ...           Event(name='Talk 7', event_type='talk', duration=30, roles="empty", tags=['intermediate', 'advanced'], unavailability=outside_slots, demand=60),
    ...           Event(name='Talk 8', event_type='talk', duration=30, roles="empty", tags=['intermediate', 'advanced'], unavailability=outside_slots, demand=60),
    ...           Event(name='Talk 9', event_type='talk', duration=30, roles="empty", tags=['advanced'], unavailability=outside_slots, demand=60),
    ...           Event(name='Talk 10', event_type='talk', duration=30, roles="empty", tags=['advanced'], unavailability=outside_slots, demand=30),
    ...           Event(name='Talk 11', event_type='talk', duration=30, roles="empty", tags=['advanced'], unavailability=outside_slots, demand=30),
    ...           Event(name='Talk 12', event_type='talk', duration=30, roles="empty", tags=['advanced'], unavailability=outside_slots, demand=30),
    ...           Event(name='Workshop 1', event_type='workshop', duration=60, roles="empty", tags=['testing'], unavailability=talk_slots + outside_slots, demand=300),
    ...           Event(name='Workshop 2', event_type='workshop', duration=60, roles="empty", tags=['testing'], unavailability=talk_slots + outside_slots, demand=40),
    ...           Event(name='City tour', event_type='social event', duration=90, roles="empty", tags=[], unavailability=talk_slots + workshop_slots, demand=100),
    ...           Event(name='Boardgames', event_type='social event', duration=90, roles="empty", tags=[], unavailability=talk_slots + workshop_slots, demand=20)]

Further to this we have a couple of other constraints:


- The speaker for :code:`Talk 1` is also the person delivering :code:`Workshop 1`::

        >>> events[0].unavailability.extend([events[6]])

- Also, the person running :code:`Workshop 2` is the person hosting the
  :code:`Boardgames`::

        >>> events[13].unavailability.append(events[-1])

Now that we have :code:`slots` and :code:`events` we can schedule our
event::

    >>> from conference_scheduler import scheduler
    >>> schedule = scheduler.schedule(events, slots)

This schedule is a generator::

    >>> schedule = sorted(schedule, key=lambda item: item.slot.starts_at)
    >>> for item in schedule:
    ...     print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
    Talk 3 at 15-Sep-2016 09:30 in Small
    Talk 11 at 15-Sep-2016 09:30 in Big
    Talk 4 at 15-Sep-2016 10:00 in Small
    Talk 10 at 15-Sep-2016 10:00 in Big
    Talk 5 at 15-Sep-2016 12:30 in Big
    Talk 9 at 15-Sep-2016 12:30 in Small
    Talk 6 at 15-Sep-2016 13:00 in Big
    Talk 8 at 15-Sep-2016 13:00 in Small
    Talk 1 at 16-Sep-2016 09:30 in Big
    Workshop 2 at 16-Sep-2016 09:30 in Small
    Talk 2 at 16-Sep-2016 10:00 in Big
    Talk 7 at 16-Sep-2016 12:30 in Big
    City tour at 16-Sep-2016 12:30 in Outside
    Talk 12 at 16-Sep-2016 13:00 in Big
    Workshop 1 at 16-Sep-2016 13:00 in Small
    Boardgames at 16-Sep-2016 13:00 in Outside



We see that all the events are scheduled in appropriate rooms (as indicated by
the unavailability attribute for the events). Also we have that :code:`Talk 1`
doesn't class with :code:`Workshop 1`.
Similarly, the :code:`Boardgame` does not clash with :code:`Workshop 2`.

You will also note that in any given session, talks share at least one tag. This
is another constraint of the model, if you find that your schedule has no
solutions you can adjust it by recategorising your talks (or giving them all a
single category).

The data we input in to the model included information about demand for a talk,
this could be approximated from previous popularity for a talk. However, the
scheduler has put :code:`Talk 3` (which has high demand) in the small room
(which has capacity 50). We can include an objective function in to our
scheduler to aim to minimise the difference between room capacity and demand::

    >>> from conference_scheduler.lp_problem import objective_functions
    >>> func = objective_functions.capacity_demand_difference
    >>> schedule = scheduler.schedule(events, slots, objective_function=func)

    >>> schedule = sorted(schedule, key=lambda item: item.slot.starts_at)
    >>> for item in schedule:
    ...     print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
    Talk 1 at 15-Sep-2016 09:30 in Big
    Talk 12 at 15-Sep-2016 09:30 in Small
    Talk 3 at 15-Sep-2016 10:00 in Big
    Talk 11 at 15-Sep-2016 10:00 in Small
    Talk 4 at 15-Sep-2016 12:30 in Small
    Talk 10 at 15-Sep-2016 12:30 in Big
    Talk 2 at 15-Sep-2016 13:00 in Small
    Talk 9 at 15-Sep-2016 13:00 in Big
    Talk 7 at 16-Sep-2016 09:30 in Big
    Workshop 2 at 16-Sep-2016 09:30 in Small
    Talk 6 at 16-Sep-2016 10:00 in Big
    Talk 8 at 16-Sep-2016 12:30 in Big
    City tour at 16-Sep-2016 12:30 in Outside
    Talk 5 at 16-Sep-2016 13:00 in Big
    Workshop 1 at 16-Sep-2016 13:00 in Small
    Boardgames at 16-Sep-2016 13:00 in Outside


We see that :code:`Talk 3` has moved to the bigger room but that all other
constraints still hold.
