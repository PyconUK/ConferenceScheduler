from typing import NamedTuple
from datetime import datetime


class Demand(NamedTuple):
    event: Event
    audience: int


class Event(NamedTuple):
    name: str
    type: EventType


class EventType(NamedTuple):
    name: str


class Person(NamedTuple):
    name: str


class Role(NamedTuple):
    name: str


class Room(NamedTuple):
    name: str
    capacity: int


class Session(NamedTuple)
    slots: Sequence[Slot]


class Slot(NamedTuple):
    starts_at: datetime
    ends_at: datetime


class Unavailability(NamedTuple):
    person: Person
    slot: Slot
