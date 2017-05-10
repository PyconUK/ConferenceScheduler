Define a Conference
===================

Using PyCon UK 2016 for example data, let us consider how we might define a
conference and pass the necessary data to the scheduler.

In 2016, there were three types of event: talks, workshops and plenary sessions
and these were held in five rooms at Cardiff City Hall. Not all the rooms were
suitable for all types event.

We can capture this information using a Python list and dictionary::

    >>> event_types = ('talk', 'workshop', 'plenary')
    >>>
    >>> venues = {
    ...     'Assembly Room': {
    ...         'capacity': 500,
    ...         'suitable_for': ['talk', 'plenary']
    ...     },
    ...     'Room A': {
    ...         'capacity': 80,
    ...         'suitable_for': ['workshop']
    ...     },
    ...     'Ferrier Hall': {
    ...         'capacity': 200,
    ...         'suitable_for': ['talk']
    ...     },
    ...     'Room C': {
    ...         'capacity': 80,
    ...         'suitable_for': ['talk', 'workshop']
    ...     },
    ...     'Room D': {
    ...         'capacity': 100,
    ...         'suitable_for': ['talk']
    ...     },
    ... }

The events took place over the course of three days in September, but the
workshops only occurred on the final day.

Here is how we might represent this information using JSON::

    >>> import json
    >>>
    >>> days = json.loads("""
    ...     {
    ...         "16-Sep-2016": {"event_types": ["talk", "plenary"]},
    ...         "17-Sep-2016": {"event_types": ["talk", "plenary"]},
    ...         "18-Sep-2016": {"event_types": ["talk", "plenary", "workshop"]}
    ...     }
    ... """)

The time periods available for the three event types were not the same and they
were also grouped for talks but not for the other two.

This time using YAML, here is how we might represent that information::

    >>> import yaml
    >>>
    >>> session_times = yaml.load("""
    ...     talk:
    ...         morning:
    ...         -
    ...             starts_at: 10:15:00
    ...             duration: 30
    ...         -
    ...             starts_at: 11:15:00
    ...             duration: 45
    ...         -
    ...             starts_at: 12:00:00
    ...             duration: 30
    ...         afternoon:
    ...         -
    ...             starts_at: 12:30:00
    ...             duration: 30
    ...         -
    ...             starts_at: 14:30:00
    ...             duration: 30
    ...         -
    ...             starts_at: 15:00:00
    ...             duration: 30
    ...         -
    ...             starts_at: 15:30:00
    ...             duration: 30
    ...         evening:
    ...         -
    ...             starts_at: 16:30:00
    ...             duration: 30
    ...         -
    ...             starts_at: 17:00:00
    ...             duration: 30
    ...     workshop:
    ...         all:
    ...         -
    ...             starts_at: 10:15:00
    ...             duration: 90
    ...         -
    ...             starts_at: 11:15:00
    ...             duration: 105
    ...         -
    ...             starts_at: 14:30:00
    ...             duration: 90
    ...         -
    ...             starts_at: 16:30:00
    ...             duration: 60
    ...     plenary:
    ...         all:
    ...         -
    ...             starts_at: 09:10:00
    ...             duration: 50
    ... """)

And, of course, there are also events which need to be scheduled. Here, we have
an example of how to load a file (in this case, in YAML format) which holds the
details of the talks which took place in Cardiff::

    >>> with open('docs/howtos/pyconuk-2016-talks.yml', 'r') as file:
    ...     talks = yaml.load(file)

The structure in which we have defined our session times is convenient and
readable, but it's not the structure required by the scheduler. Instead, we
need to flatten it so that we have the start time, duration and session name
in one tuple. We'll create a dictionary of these with the event type as a key
as we'll need each associated list of tuples separately later on::

    >>> slot_times = {
    ...     event_type: [
    ...         {
    ...             'starts_at': slot_time['starts_at'],
    ...             'duration': slot_time['duration'],
    ...             'session_name': session_name
    ...         }
    ...         for session_name, slot_times in session_times[event_type].items()
    ...         for slot_time in slot_times
    ...     ]
    ...     for event_type in event_types
    ... }

And now, we can use the data we have defined to create instances of
:code:`conference_scheduler.resources.Slot`. Again, we'll create a dictionary
of those with the event type as key because we'll need each list of Slots
separately later on::

    >>> import itertools as it
    >>> from conference_scheduler.resources import Slot
    >>>
    >>> slots = {
    ...     event_type: [
    ...         Slot(
    ...             venue=venue,
    ...             starts_at=slot_time['starts_at'],
    ...             duration=slot_time['duration'],
    ...             session=slot_time['session_name'],
    ...             capacity=venues[venue]['capacity']
    ...         )
    ...         for venue, day, slot_time in it.product(
    ...             venues, days, slot_times[event_type]
    ...         )
    ...         if (event_type in venues[venue]['suitable_for'] and
    ...             event_type in days[day]['event_types'])
    ...     ]
    ...     for event_type in event_types
    ... }
