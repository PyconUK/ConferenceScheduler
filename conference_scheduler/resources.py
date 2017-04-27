from typing import NamedTuple, Sequence
from datetime import datetime


class EventType(NamedTuple):
    name: str


class Event(NamedTuple):
    name: str
    type: EventType


class Demand(NamedTuple):
    event: Event
    audience: int


class Person(NamedTuple):
    name: str


class Role(NamedTuple):
    name: str


class Room(NamedTuple):
    name: str
    capacity: int


class Slot(NamedTuple):
    starts_at: datetime
    ends_at: datetime


class ScheduledItem(NamedTuple):
    event: Event
    room: Room
    slot: Slot


class Session(NamedTuple):
    slots: Sequence[Slot]


class Unavailability(NamedTuple):
    person: Person
    slot: Slot
