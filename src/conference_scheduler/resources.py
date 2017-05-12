from typing import NamedTuple
from datetime import datetime


class Slot(NamedTuple):
    venue: str
    starts_at: datetime
    duration: int
    capacity: int
    session: str


class Event:

    def __init__(self, name, duration, demand, tags=None, unavailability=None):
        self.name = name
        self.duration = duration
        self.demand = demand
        if tags is None:
            tags = []
        self.tags = tags
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

    def add_unavailability(self, object):
        try:
            self._unavailability.extend(object)
        except TypeError:
            self._unavailability.append(object)

    def remove_unavailability(self, object):
        self._unavailability.remove(object)


class ScheduledItem(NamedTuple):
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
