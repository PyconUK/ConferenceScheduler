Tutorial
========

Welcome! You are the head scheduler for the upcoming :code:`name` con. You have
a venue, you have talks and you have a week to schedule everything!

Your venue has two rooms in which you will schedule talks and workshops in
parallel but you're also going to want to find time for some social events.

You have organised your time slots as follows:

- The first day will have 2 sessions (morning and afternoon) with 2 30 minute
  time slots in each room.
- The second day will have 1 room used for longer 1 hour talks and 2 long
  sessions set aside for the social events.

Let us create these time slots using the :code:`conference_scheduler`::

    >>> import conference_scheduler as cs

    >>> rooms = [cs.resources.Room(name="Big", capacity="200", suitability=[]),
    ...          cs.resources.Room(name="Small", capacity="50", suitability=[]),
    ...          cs.resources.Room(name="outside", capacity="1000", suitability=[])]
    >>> slots = [cs.resources.Slot(room=rooms[0], starts_at='15-Sep-2016 09:30', duration=30, session="A"),
    ...          cs.resources.Slot(room=rooms[0], starts_at='15-Sep-2016 10:00', duration=30, session="A"),
    ...          cs.resources.Slot(room=rooms[1], starts_at='15-Sep-2016 09:30', duration=30, session="B"),
    ...          cs.resources.Slot(room=rooms[1], starts_at='15-Sep-2016 10:00', duration=30, session="B"),
    ...          cs.resources.Slot(room=rooms[0], starts_at='15-Sep-2016 12:30', duration=30, session="C"),
    ...          cs.resources.Slot(room=rooms[0], starts_at='15-Sep-2016 13:00', duration=30, session="C"),
    ...          cs.resources.Slot(room=rooms[1], starts_at='16-Sep-2016 09:30', duration=60, session="E"),
    ...          cs.resources.Slot(room=rooms[1], starts_at='16-Sep-2016 13:00', duration=60, session="F"),
    ...          cs.resources.Slot(room=rooms[2], starts_at='16-Sep-2016 12:30', duration=30, session="G"),
    ...          cs.resources.Slot(room=rooms[2], starts_at='16-Sep-2016 13:00', duration=30, session="H")]
