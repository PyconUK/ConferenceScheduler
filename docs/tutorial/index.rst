.. _tutorial:

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

Installing the conference scheduler
-----------------------------------

**The conference scheduler is compatible with Python 3.6+ only.**

You can install the latest version of :code:`conference_scheduler` from PyPI::

    $ pip install conference_scheduler

If you want to, you can also install a development version from source::

    $ git clone https://github.com/PyconUK/ConferenceScheduler
    $ cd ConferenceScheduler
    $ python setup.py develop

Inputting the data
------------------


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

**Note** that the :code:`starts_at` format must be :code:`'%d-%b-%Y %H:%M'` and that
:code:`duration` must be given in minutes.

We also have a number of talks and workshops to schedule, because of the
duration/location of the slots we know some of them are unavailable for a given slot::

    >>> events = [Event(name='Talk 1', duration=30, tags=['beginner'], unavailability=outside_slots[:], demand=50),
    ...           Event(name='Talk 2', duration=30, tags=['beginner'], unavailability=outside_slots[:], demand=130),
    ...           Event(name='Talk 3', duration=30, tags=['beginner'], unavailability=outside_slots[:], demand=500),
    ...           Event(name='Talk 4', duration=30, tags=['beginner'], unavailability=outside_slots[:], demand=30),
    ...           Event(name='Talk 5', duration=30, tags=['intermediate'], unavailability=outside_slots[:], demand=60),
    ...           Event(name='Talk 6', duration=30, tags=['intermediate'], unavailability=outside_slots[:], demand=30),
    ...           Event(name='Talk 7', duration=30, tags=['intermediate', 'advanced'], unavailability=outside_slots[:], demand=60),
    ...           Event(name='Talk 8', duration=30, tags=['intermediate', 'advanced'], unavailability=outside_slots[:], demand=60),
    ...           Event(name='Talk 9', duration=30, tags=['advanced'], unavailability=outside_slots[:], demand=60),
    ...           Event(name='Talk 10', duration=30, tags=['advanced'], unavailability=outside_slots[:], demand=30),
    ...           Event(name='Talk 11', duration=30, tags=['advanced'], unavailability=outside_slots[:], demand=30),
    ...           Event(name='Talk 12', duration=30, tags=['advanced'], unavailability=outside_slots[:], demand=30),
    ...           Event(name='Workshop 1', duration=60, tags=['testing'], unavailability=outside_slots[:], demand=300),
    ...           Event(name='Workshop 2', duration=60, tags=['testing'], unavailability=outside_slots[:], demand=40),
    ...           Event(name='City tour', duration=90, tags=[], unavailability=talk_slots[:] + workshop_slots[:], demand=100),
    ...           Event(name='Boardgames', duration=90, tags=[], unavailability=talk_slots[:] + workshop_slots[:], demand=20)]

Further to this we have a couple of other constraints:

- The speaker for :code:`Talk 1` is also the person delivering :code:`Workshop 1`::

        >>> events[0].add_unavailability(events[6])

- Also, the person running :code:`Workshop 2` is the person hosting the
  :code:`Boardgames`::

        >>> events[13].add_unavailability(events[-1])

Note that we haven't indicated the workshops cannot happen in the talk slots but
this will automatically be taken care of because of the duration of the
workshops (60mins) and the duration of the talk slots (30mins).

Creating a schedule
-------------------

Now that we have :code:`slots` and :code:`events` we can schedule our
event::

    >>> from conference_scheduler import scheduler
    >>> schedule = scheduler.schedule(events, slots)

    >>> schedule.sort(key=lambda item: item.slot.starts_at)
    >>> for item in schedule:
    ...     print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
    Talk 3 at 15-Sep-2016 09:30 in Small
    Talk 11 at 15-Sep-2016 09:30 in Big
    Talk 4 at 15-Sep-2016 10:00 in Small
    Talk 8 at 15-Sep-2016 10:00 in Big
    Talk 1 at 15-Sep-2016 12:30 in Small
    Talk 5 at 15-Sep-2016 12:30 in Big
    Talk 2 at 15-Sep-2016 13:00 in Small
    Talk 6 at 15-Sep-2016 13:00 in Big
    Talk 9 at 16-Sep-2016 09:30 in Big
    Workshop 2 at 16-Sep-2016 09:30 in Small
    Talk 10 at 16-Sep-2016 10:00 in Big
    Talk 7 at 16-Sep-2016 12:30 in Big
    Boardgames at 16-Sep-2016 12:30 in Outside
    Talk 12 at 16-Sep-2016 13:00 in Big
    Workshop 1 at 16-Sep-2016 13:00 in Small
    City tour at 16-Sep-2016 13:00 in Outside

We see that all the events are scheduled in appropriate rooms (as indicated by
the unavailability attribute for the events). Also we have that :code:`Talk 1`
doesn't clash with :code:`Workshop 1`.
Similarly, the :code:`Boardgame` does not clash with :code:`Workshop 2`.

You will also note that in any given session, talks share at least one tag. This
is another constraint of the model; if you find that your schedule has no
solutions you can adjust it by re-categorising your talks (or giving them all a
single category).

Avoiding room overcrowding
--------------------------

The data we input in to the model included information about demand for a talk;
this could be approximated from previous popularity for a talk. However, the
scheduler has put :code:`Talk 2` and :code:`Talk 3` (which have high demand) in
the small room (which has capacity 50). We can include an objective function in
our scheduler to minimise the difference between room capacity and demand::

    >>> from conference_scheduler.lp_problem import objective_functions
    >>> func = objective_functions.capacity_demand_difference
    >>> schedule = scheduler.schedule(events, slots, objective_function=func)

    >>> schedule.sort(key=lambda item: item.slot.starts_at)
    >>> for item in schedule:
    ...     print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
    Talk 4 at 15-Sep-2016 09:30 in Big
    Talk 7 at 15-Sep-2016 09:30 in Small
    Talk 1 at 15-Sep-2016 10:00 in Big
    Talk 6 at 15-Sep-2016 10:00 in Small
    Talk 8 at 15-Sep-2016 12:30 in Big
    Talk 12 at 15-Sep-2016 12:30 in Small
    Talk 5 at 15-Sep-2016 13:00 in Big
    Talk 10 at 15-Sep-2016 13:00 in Small
    Talk 3 at 16-Sep-2016 09:30 in Big
    Workshop 2 at 16-Sep-2016 09:30 in Small
    Talk 2 at 16-Sep-2016 10:00 in Big
    Talk 11 at 16-Sep-2016 12:30 in Big
    Boardgames at 16-Sep-2016 12:30 in Outside
    Talk 9 at 16-Sep-2016 13:00 in Big
    Workshop 1 at 16-Sep-2016 13:00 in Small
    City tour at 16-Sep-2016 13:00 in Outside


We see that those talks have moved to the bigger room but that all other
constraints still hold.

Coping with new information
---------------------------

This is fantastic! Our schedule has now been published and everyone is excited
about the conference. However, as can often happen, one of the speakers now
informs us of a particular new constraints. For example, the speaker for
:code:`Talk 11` is unable to speak on the first day.

We can enter this new constraint::

    >>> events[10].add_unavailability(*slots[9:])

We can now solve the problem one more time from scratch just as before::

    >>> alt_schedule = scheduler.schedule(events, slots, objective_function=func)

    >>> alt_schedule.sort(key=lambda item: item.slot.starts_at)
    >>> for item in alt_schedule:
    ...     print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
    Talk 1 at 15-Sep-2016 09:30 in Big
    Talk 8 at 15-Sep-2016 09:30 in Small
    Talk 4 at 15-Sep-2016 10:00 in Big
    Talk 5 at 15-Sep-2016 10:00 in Small
    Talk 3 at 15-Sep-2016 12:30 in Small
    Talk 9 at 15-Sep-2016 12:30 in Big
    Talk 2 at 15-Sep-2016 13:00 in Small
    Talk 12 at 15-Sep-2016 13:00 in Big
    Talk 11 at 16-Sep-2016 09:30 in Big
    Workshop 2 at 16-Sep-2016 09:30 in Small
    Talk 10 at 16-Sep-2016 10:00 in Big
    Talk 6 at 16-Sep-2016 12:30 in Big
    Boardgames at 16-Sep-2016 12:30 in Outside
    Talk 7 at 16-Sep-2016 13:00 in Big
    Workshop 1 at 16-Sep-2016 13:00 in Small
    City tour at 16-Sep-2016 13:00 in Outside

This has resulted in a
completely different schedule with a number of changes. We can however solve the
problem with a new objective function which is to minimise the changes from the
old schedule::


    >>> func = objective_functions.number_of_changes
    >>> similar_schedule = scheduler.schedule(events, slots, objective_function=func, original_schedule=schedule)

    >>> similar_schedule.sort(key=lambda item: item.slot.starts_at)
    >>> for item in similar_schedule:
    ...     print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
    Talk 4 at 15-Sep-2016 09:30 in Big
    Talk 7 at 15-Sep-2016 09:30 in Small
    Talk 1 at 15-Sep-2016 10:00 in Big
    Talk 6 at 15-Sep-2016 10:00 in Small
    Talk 8 at 15-Sep-2016 12:30 in Big
    Talk 11 at 15-Sep-2016 12:30 in Small
    Talk 5 at 15-Sep-2016 13:00 in Big
    Talk 10 at 15-Sep-2016 13:00 in Small
    Talk 3 at 16-Sep-2016 09:30 in Big
    Workshop 2 at 16-Sep-2016 09:30 in Small
    Talk 2 at 16-Sep-2016 10:00 in Big
    Talk 12 at 16-Sep-2016 12:30 in Big
    Boardgames at 16-Sep-2016 12:30 in Outside
    Talk 9 at 16-Sep-2016 13:00 in Big
    Workshop 1 at 16-Sep-2016 13:00 in Small
    City tour at 16-Sep-2016 13:00 in Outside



Spotting the Changes
--------------------
It can be a little difficult to spot what has changed when we compute a new schedule and so
there are two functions which can help. Let's take our :code:`alt_schedule` and compare it
with the original. Firstly, we can see which events moved to different slots::


    >>> event_diff = scheduler.event_schedule_difference(schedule, alt_schedule)
    >>> for item in event_diff:
    ...     print(f"{item.event.name} has moved from {item.old_slot.venue} at {item.old_slot.starts_at} to {item.new_slot.venue} at {item.new_slot.starts_at}")
    Talk 1 has moved from Big at 15-Sep-2016 10:00 to Big at 15-Sep-2016 09:30
    Talk 10 has moved from Small at 15-Sep-2016 13:00 to Big at 16-Sep-2016 10:00
    Talk 11 has moved from Big at 16-Sep-2016 12:30 to Big at 16-Sep-2016 09:30
    Talk 12 has moved from Small at 15-Sep-2016 12:30 to Big at 15-Sep-2016 13:00
    Talk 2 has moved from Big at 16-Sep-2016 10:00 to Small at 15-Sep-2016 13:00
    Talk 3 has moved from Big at 16-Sep-2016 09:30 to Small at 15-Sep-2016 12:30
    Talk 4 has moved from Big at 15-Sep-2016 09:30 to Big at 15-Sep-2016 10:00
    Talk 5 has moved from Big at 15-Sep-2016 13:00 to Small at 15-Sep-2016 10:00
    Talk 6 has moved from Small at 15-Sep-2016 10:00 to Big at 16-Sep-2016 12:30
    Talk 7 has moved from Small at 15-Sep-2016 09:30 to Big at 16-Sep-2016 13:00
    Talk 8 has moved from Big at 15-Sep-2016 12:30 to Small at 15-Sep-2016 09:30
    Talk 9 has moved from Big at 16-Sep-2016 13:00 to Big at 15-Sep-2016 12:30


We can also look at slots to see which now have a different event scheduled::

    >>> slot_diff = scheduler.slot_schedule_difference(schedule, alt_schedule)
    >>> for item in slot_diff:
    ...     print(f"{item.slot.venue} at {item.slot.starts_at} will now host {item.new_event.name} rather than {item.old_event.name}" )
    Big at 15-Sep-2016 09:30 will now host Talk 1 rather than Talk 4
    Big at 15-Sep-2016 10:00 will now host Talk 4 rather than Talk 1
    Big at 15-Sep-2016 12:30 will now host Talk 9 rather than Talk 8
    Big at 15-Sep-2016 13:00 will now host Talk 12 rather than Talk 5
    Big at 16-Sep-2016 09:30 will now host Talk 11 rather than Talk 3
    Big at 16-Sep-2016 10:00 will now host Talk 10 rather than Talk 2
    Big at 16-Sep-2016 12:30 will now host Talk 6 rather than Talk 11
    Big at 16-Sep-2016 13:00 will now host Talk 7 rather than Talk 9
    Small at 15-Sep-2016 09:30 will now host Talk 8 rather than Talk 7
    Small at 15-Sep-2016 10:00 will now host Talk 5 rather than Talk 6
    Small at 15-Sep-2016 12:30 will now host Talk 3 rather than Talk 12
    Small at 15-Sep-2016 13:00 will now host Talk 2 rather than Talk 10


We can use this facility to show how using :code:`number_of_changes` as our objective function
resulted in far fewer changes::

    >>> event_diff = scheduler.event_schedule_difference(schedule, similar_schedule)
    >>> for item in event_diff:
    ...     print(f"{item.event.name} has moved from {item.old_slot.venue} at {item.old_slot.starts_at} to {item.new_slot.venue} at {item.new_slot.starts_at}")
    Talk 11 has moved from Big at 16-Sep-2016 12:30 to Small at 15-Sep-2016 12:30
    Talk 12 has moved from Small at 15-Sep-2016 12:30 to Big at 16-Sep-2016 12:30


Scheduling chairs
-----------------

Once we have a schedule for our talks, workshops and social events, we have the
last task which is to schedule chairs for the talk sessions.

We have 6 different sessions of talks to chair::

    Talk 4 at 15-Sep-2016 09:30 in Big
    Talk 1 at 15-Sep-2016 10:00 in Big

    Talk 7 at 15-Sep-2016 09:30 in Small
    Talk 6 at 15-Sep-2016 10:00 in Small

    Talk 8 at 15-Sep-2016 12:30 in Big
    Talk 5 at 15-Sep-2016 13:00 in Big

    Talk 11 at 15-Sep-2016 12:30 in Small
    Talk 10 at 15-Sep-2016 13:00 in Small

    Talk 3 at 16-Sep-2016 09:30 in Big
    Talk 2 at 16-Sep-2016 10:00 in Big

    Talk 12 at 16-Sep-2016 12:30 in Big
    Talk 9 at 16-Sep-2016 13:00 in Big

We will use the conference scheduler, with these sessions corresponding
to slots::


    >>> chair_slots  = [Slot(venue='Big', starts_at='15-Sep-2016 09:30', duration=60, session="A", capacity=200),
    ...                 Slot(venue='Small', starts_at='15-Sep-2016 09:30', duration=60, session="B", capacity=50),
    ...                 Slot(venue='Big', starts_at='15-Sep-2016 12:30', duration=60, session="C", capacity=200),
    ...                 Slot(venue='Small', starts_at='15-Sep-2016 12:30', duration=60, session="D", capacity=50),
    ...                 Slot(venue='Big', starts_at='16-Sep-2016 12:30', duration=60, session="E", capacity=200),
    ...                 Slot(venue='Small', starts_at='16-Sep-2016 12:30', duration=60, session="F", capacity=50)]

We will need 6 chairpersons for these slots and we will use events as chairs. In
practice, all chairing will be taken care of by 3 people, with each person
chairing 2 sessions::

    >>> events = [Event(name='Chair A-1', duration=60, demand=0),
    ...           Event(name='Chair A-2', duration=60, demand=0),
    ...           Event(name='Chair B-1', duration=60, demand=0),
    ...           Event(name='Chair B-2', duration=60, demand=0),
    ...           Event(name='Chair C-1', duration=60, demand=0),
    ...           Event(name='Chair D-2', duration=60, demand=0)]


As you can see, we have set all unavailabilities to be empty however
:code:`Chair A` is in fact the speaker for :code:`Talk 11`. Also :code:`Chair B`
has informed us that they are not present on the first day. We can include these
constraints::

    >>> events[0].add_unavailability(chair_slots[4])
    >>> events[1].add_unavailability(chair_slots[4])
    >>> events[2].add_unavailability(*chair_slots[4:])
    >>> events[3].add_unavailability(*chair_slots[4:])

Finally, each chair cannot chair more than one session at a time::


    >>> events[0].add_unavailability(events[1])
    >>> events[2].add_unavailability(events[3])
    >>> events[4].add_unavailability(events[5])

Now let us get the chair schedule::

    >>> chair_schedule = scheduler.schedule(events, chair_slots)

    >>> chair_schedule.sort(key=lambda item: item.slot.starts_at)
    >>> for item in chair_schedule:
    ...     print(f"{item.event.name} chairing {item.slot.starts_at} in {item.slot.venue}")
    Chair A-2 chairing 15-Sep-2016 09:30 in Big
    Chair B-1 chairing 15-Sep-2016 09:30 in Small
    Chair B-2 chairing 15-Sep-2016 12:30 in Small
    Chair C-1 chairing 15-Sep-2016 12:30 in Big
    Chair A-1 chairing 16-Sep-2016 12:30 in Small
    Chair D-2 chairing 16-Sep-2016 12:30 in Big


Validating a schedule
---------------------

It might of course be helpful to use the tool simply to check if a given
schedule is correct: perhaps someone makes a manual change and it is desirable
to verify that this is still a valid schedule. Let us first check that our
schedule obtained from the algorithm is correct::

    >>> from conference_scheduler.validator import is_valid_schedule, schedule_violations
    >>> is_valid_schedule(chair_schedule, events=events, slots=chair_slots)
    True

Let us modify our schedule so that it schedules an event twice::

    >>> from conference_scheduler.resources import ScheduledItem
    >>> chair_schedule[0] = ScheduledItem(event=events[2], slot=chair_slots[0])
    >>> for item in chair_schedule[:2]:
    ...     print(f"{item.event.name} chairing {item.slot.starts_at} in {item.slot.venue}")
    Chair B-1 chairing 15-Sep-2016 09:30 in Big
    Chair B-1 chairing 15-Sep-2016 09:30 in Small

We now see that we have an invalid schedule::

    >>> is_valid_schedule(chair_schedule, events=events, slots=chair_slots)
    False

We can furthermore identify which constraints were broken::

    >>> for v in schedule_violations(chair_schedule, events=events, slots=chair_slots):
    ...     print(v)
    Event either not scheduled or scheduled multiple times - event: 1
    Event either not scheduled or scheduled multiple times - event: 2
