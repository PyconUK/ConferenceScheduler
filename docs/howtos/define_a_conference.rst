Define a Conference
===================

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

>>> import json
>>>
>>> days = json.loads("""
...     {
...         "16-Sep-2016": {"event_types": ["talk", "plenary"]},
...         "17-Sep-2016": {"event_types": ["talk", "plenary"]},
...         "18-Sep-2016": {"event_types": ["talk", "plenary", "workshop"]}
...     }
... """)

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

>>> with open('docs/howtos/pyconuk-2016-talks.yml', 'r') as file:
...     talks = yaml.load(file)

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
