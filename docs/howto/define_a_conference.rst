Define a Conference
===================

Using PyCon UK 2016 for example data, let us consider how we might define a
conference and pass the necessary data to the scheduler.

The aim here is to show how we might use simple data structures and formats
to hold the information we require and then parse and process those structures
into the necessary form for the scheduler.

We'll use a variety of simple Python data types, YAML and JSON documents and
we'll include both inline data and external files. This is simply by way of
example and it's likely that a real application would standardise on far fewer
of those options than are shown here.

Data Structures
---------------

In 2016, there were three types of event: talks, workshops and plenary sessions
and these were held in five rooms at Cardiff City Hall. Not all the rooms were
suitable for all types event.

We can capture this information using a Python list and dictionary::

    >>> event_types = ('talk', 'workshop', 'plenary')

    >>> venues = {
    ...     'Assembly Room': {'capacity': 500, 'suitable_for': ['talk', 'plenary']},
    ...     'Room A': {'capacity': 80, 'suitable_for': ['workshop']},
    ...     'Ferrier Hall': {'capacity': 200, 'suitable_for': ['talk']},
    ...     'Room C': {'capacity': 80, 'suitable_for': ['talk', 'workshop']},
    ...     'Room D': {'capacity': 100, 'suitable_for': ['talk']}}

The events took place over the course of five days in September but, for this
example, we are not considering the first day of the conference (Thursday) or
the last (Monday). There were talks given on all three of those days (Friday to
Sunday) but the workshops only took place on the Sunday.

Here is how we might represent this information using JSON::

    >>> import json

    >>> json_days = """{
    ...     "16-Sep-2016": {"event_types": ["talk", "plenary"]},
    ...     "17-Sep-2016": {"event_types": ["talk", "plenary"]},
    ...     "18-Sep-2016": {"event_types": ["talk", "plenary", "workshop"]}}"""

The time periods available for the three event types were not the same and they
were also grouped for talks but not for the other two.

This time using YAML, here is how we might represent that information::

    >>> yaml_session_times = """
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
    ...         None:
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
    ...         None:
    ...         -
    ...             starts_at: 9:10:00
    ...             duration: 50"""

Next, we have the events which need to be scheduled. For this example, we have
the talks that were accepted for PyConUK 2016 in a
:download:`YAML file <pyconuk-2016-talks.yml>`

Loading into Python
-------------------

Since we used a Python list and dictionary for the event types and venues,
those are already available to us.

Next, we need to load the JSON and YAML data so that it too becomes available
as lists and dictionaries. First, let's load the JSON document which holds the
'days' information. We'll include a function to convert the strings
representing the dates into proper Python datetime objects.::

    >>> import json
    >>> from datetime import datetime
    >>> from pprint import PrettyPrinter

    >>> def date_decoder(day):
    ...    for key in day.keys():
    ...        try:
    ...            new_key = datetime.strptime(key, '%d-%b-%Y')
    ...            day[new_key] = day[key]
    ...            del day[key]
    ...        except:
    ...            pass
    ...    return day
    >>>
    >>> days = json.loads(json_days, object_hook=date_decoder)

    >>> pp = PrettyPrinter()
    >>> pp.pprint(days)
    {datetime.datetime(2016, 9, 16, 0, 0): {'event_types': ['talk', 'plenary']},
     datetime.datetime(2016, 9, 17, 0, 0): {'event_types': ['talk', 'plenary']},
     datetime.datetime(2016, 9, 18, 0, 0): {'event_types': ['talk',
                                                            'plenary',
                                                            'workshop']}}

We can load the YAML document containing the 'session times' information in a
similar fashion. Again, the data is loaded into a Python dictionary with each
event type as a key mapping to a further dictionary with the session name as
key and a list of slot times as its values. The start times are converted to an
integer representing the number of seconds since midnight::

    >>> import yaml

    >>> session_times = yaml.load(yaml_session_times)

    >>> pp.pprint(session_times['workshop'])
    {'None': [{'duration': 90, 'starts_at': 36900},
              {'duration': 105, 'starts_at': 40500},
              {'duration': 90, 'starts_at': 52200},
              {'duration': 60, 'starts_at': 59400}]}

And also the file containing the talks::

    >>> with open('docs/howto/pyconuk-2016-talks.yml', 'r') as file:
    ...     talks = yaml.load(file)

    >>> pp.pprint(talks[0:3])
    [{'duration': 30,
      'speaker': 'Kevin Keenoy',
      'title': 'Transforming the government’s Digital Marketplace from portal to '
               'platform'},
     {'duration': 45,
      'speaker': 'Tom Christie',
      'title': 'Django REST framework: Schemas, Hypermedia & Client libraries.'},
     {'duration': 30,
      'speaker': 'Iacopo Spalletti',
      'title': 'django CMS in the real time web: how to mix CMS, websockets, REST '
               'for a fully real time experience'}]

Processing
----------

Before we can compute a schedule for our conference, we need to create the
:code:`Event` and :code:`Slot` objects required by the scheduler.

Slots
*****

The nested structure we have used to define our session times is convenient and
readable, but it's not the structure required by the scheduler. Instead, we
need to flatten it so that we have the start time, duration and session name
at the same level. We'll create a dictionary of these with the event type as a
key as we'll need each associated list separately later on::

    >>> slot_times = {
    ...     event_type: [{
    ...         'starts_at': slot_time['starts_at'],
    ...         'duration': slot_time['duration'],
    ...         'session_name': session_name}
    ...         for session_name, slot_times in session_times[event_type].items()
    ...         for slot_time in slot_times]
    ...     for event_type in event_types}

    >>> pp.pprint(slot_times['workshop'])
    [{'duration': 90, 'session_name': 'None', 'starts_at': 36900},
     {'duration': 105, 'session_name': 'None', 'starts_at': 40500},
     {'duration': 90, 'session_name': 'None', 'starts_at': 52200},
     {'duration': 60, 'session_name': 'None', 'starts_at': 59400}]

Now, we can use that flattened structure to create instances of
:code:`conference_scheduler.resources.Slot`. A :code:`Slot` instance represents
a time and a place into which an event can be scheduled. We'll combine the
:code:`slot_times` dictionary with the :code:`days` list and the :code:`venues`
dictionary to give us all the possible combinations.

Again, we'll create a dictionary of those with the event type as key because
we'll need each list of :code:`Slots` separately later on::

    >>> import itertools as it
    >>> from datetime import timedelta
    >>> from conference_scheduler.resources import Slot

    >>> slots = {
    ...     event_type: [
    ...         Slot(
    ...             venue=venue,
    ...             starts_at=day + timedelta(0, slot_time['starts_at']),
    ...             duration=slot_time['duration'],
    ...             session=f"{day.date()} {slot_time['session_name']}",
    ...             capacity=venues[venue]['capacity'])
    ...         for venue, day, slot_time in it.product(
    ...             venues, days, slot_times[event_type])
    ...         if (event_type in venues[venue]['suitable_for'] and
    ...             event_type in days[day]['event_types'])]
    ...     for event_type in event_types}

    >>> pp.pprint(slots['talk'][0:5])
    [Slot(venue='Assembly Room', starts_at=datetime.datetime(2016, 9, 16, 10, 15), duration=30, capacity=500, session='2016-09-16 morning'),
     Slot(venue='Assembly Room', starts_at=datetime.datetime(2016, 9, 16, 11, 15), duration=45, capacity=500, session='2016-09-16 morning'),
     Slot(venue='Assembly Room', starts_at=datetime.datetime(2016, 9, 16, 12, 0), duration=30, capacity=500, session='2016-09-16 morning'),
     Slot(venue='Assembly Room', starts_at=datetime.datetime(2016, 9, 16, 12, 30), duration=30, capacity=500, session='2016-09-16 afternoon'),
     Slot(venue='Assembly Room', starts_at=datetime.datetime(2016, 9, 16, 14, 30), duration=30, capacity=500, session='2016-09-16 afternoon')]

Events
******

For our talks, we can use the list we've loaded to create instances of
:code:`conference_scheduler.resources.Event`. Once again, we'll create a
dictionary with the event type as the keys::

    >>> from conference_scheduler.resources import Event
    >>>
    >>> events = {
    ...     'talk': [
    ...         Event(talk['title'], talk['duration'], demand=None, tags=talk.get('tags', None))
    ...         for talk in talks]}

    >>> pp.pprint(events['talk'][0:3])
    [Event(name='Transforming the government’s Digital Marketplace from portal to platform', duration=30, demand=None, tags=[], unavailability=[]),
     Event(name='Django REST framework: Schemas, Hypermedia & Client libraries.', duration=45, demand=None, tags=[], unavailability=[]),
     Event(name='django CMS in the real time web: how to mix CMS, websockets, REST for a fully real time experience', duration=30, demand=None, tags=[], unavailability=[])]
