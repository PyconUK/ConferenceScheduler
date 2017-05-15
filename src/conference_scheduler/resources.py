from typing import NamedTuple
from datetime import datetime


class Slot(NamedTuple):
    """A period of time at a venue in which an event can be scheduled

    Parameters
    ----------
    venue : str
        A human readable string
    starts_at: datetime
        The starting time for the time period
    duration: int
        The duration of the time period in minutes
    capacity: int
        This will be compared with :attr:`Event.demand` during computation of
        the schedule to ensure that events are only scheduled in slots that can
        accommodate them.
    session: str
        A human readable string which serves as a tag for similar time periods
        e.g. 'morning', 'afternoon'

    Example
    -------
    For a conference where:

        * It will take place on 2016-09-17
        * There are two rooms - 'Main Hall' and 'Small Room'
        * The Main Hall can seat 500 people and the Small Room, 50
        * It is intended to hold two 30 minute talks in the morning (from 09:30
          to 10:00 and from 11:00 to 11:30) and two more in the afternoon
          (from 14:00 to 14:30 and 15:00 to 15:30)

    We would create the following eight objects::

        >>> from conference_scheduler.resources import Slot
        >>> Slot(
        ...    venue='Main Hall', starts_at=datetime(2016, 09, 17, 09, 30),
        ...     duration=30, capacity=500, session='morning')
        >>> Slot(
        ...     venue='Main Hall', starts_at=datetime(2016, 09, 17, 10, 00),
        ...     duration=30, capacity=500, session='morning')
        >>> Slot(
        ...     venue='Main Hall', starts_at=datetime(2016, 09, 17, 14, 00),
        ...     duration=30, capacity=500, session='afternoon')
        >>> Slot(
        ...     venue='Main Hall', starts_at=datetime(2016, 09, 17, 15, 00),
        ...     duration=30, capacity=500, session='afternoon')
        >>> Slot(
        ...     venue='Small Room', starts_at=datetime(2016, 09, 17, 09, 30),
        ...     duration=30, capacity=50, session='morning')
        >>> Slot(
        ...     venue='Small Room', starts_at=datetime(2016, 09, 17, 10, 00),
        ...     duration=30, capacity=50, session='morning')
        >>> Slot(
        ...     venue='Small Room', starts_at=datetime(2016, 09, 17, 14, 00),
        ...     duration=30, capacity=50, session='afternoon')
        >>> Slot(
        ...     venue='Small Room', starts_at=datetime(2016, 09, 17, 15, 00),
        ...     duration=30, capacity=50, session='afternoon')
    """
    venue: str
    starts_at: datetime
    duration: int
    capacity: int
    session: str


class Event:
    """An event (e.g. a talk or a workshop) that needs to be scheduled

    Parameters
    ---------
    name : str
        A human readable string
    duration : int
        The expected duration of the event in minutes
    demand : int
        The anticipated demand - e.g. the number of attendees expected
        This will be compared with :attr:`Slot.capacity` during computation of
        the schedule to ensure that events are only scheduled in slots that can
        accommodate them.
        Use 0 if the event could be scheduled in any slot.
    tags : list or tuple, optional
        of human readable strings
    unavailability : list or tuple, optional
        of :class:`resources.Slot` or :class:`resources.Event`
    """

    def __init__(self, name, duration, demand, tags=None, unavailability=None):
        self.name = name
        self.duration = duration
        self.demand = demand
        if tags is None:
            tags = []
        self._tags = tags
        if unavailability is None:
            unavailability = []
        self._unavailability = unavailability

    def __repr__(self):
        return (
            f'{type(self).__name__}('
            f'name={self.name!r}, duration={self.duration!r}, '
            f'demand={self.demand!r}, tags={self.tags!r}, '
            f'unavailability={self.unavailability!r})'
        )

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return (
            self.name == other.name and
            self.duration == other.duration and
            self.demand == other.demand and
            self.tags == other.tags and
            self.unavailability == other.unavailability
        )

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(repr(self))

    @property
    def unavailability(self):
        return tuple(self._unavailability)

    def add_unavailability(self, *args):
        for arg in args:
            self._unavailability.append(arg)

    def remove_unavailability(self, object):
        self._unavailability.remove(object)

    def clear_unavailability(self):
        del self._unavailability[:]

    @property
    def tags(self):
        return tuple(self._tags)

    def add_tags(self, *args):
        for arg in args:
            self._tags.append(arg)

    def remove_tag(self, tag):
        self._tags.remove(tag)

    def clear_tags(self):
        del self._tags[:]


class ScheduledItem(NamedTuple):
    """Represents that an event has been scheduled to occur in a slot

    Parameters
    ---------
    event : :class:`resources.Event`
    slot : :class:`resources.Slot`
    """
    event: Event
    slot: Slot


class ChangedEventScheduledItem(NamedTuple):
    event: Event
    old_slot: Slot = None
    new_slot: Slot = None


class ChangedSlotScheduledItem(NamedTuple):
    slot: Slot
    old_event: Event = None
    new_event: Event = None


class Shape(NamedTuple):
    """Represents the shape of a 2 dimensional array of events and slots"""
    events: int
    slots: int


class Constraint(NamedTuple):
    label: str
    condition: bool
