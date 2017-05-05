from typing import NamedTuple, Sequence, Dict, Iterable, List
from datetime import datetime


class Slot(NamedTuple):
    venue: str
    starts_at: datetime
    duration: int
    capacity: int
    session: str


class Event(NamedTuple):
    name: str
    duration: int
    tags: List[str]
    unavailability: List
    demand: int


class ScheduledItem(NamedTuple):
    event: Event
    slot: Slot


class Shape(NamedTuple):
    """Represents the shape of a 2 dimensional array of events and slots"""
    events: int
    slots: int


class Constraint(NamedTuple):
    label: str
    condition: bool
