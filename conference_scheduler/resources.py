from typing import NamedTuple, Sequence, Dict, Iterable
from datetime import datetime


class EventType(NamedTuple):
    name: str


class Role(NamedTuple):
    name: str


CHAIR = Role(name='chair')


class Person(NamedTuple):
    name: str
    max_chair_sessions: int = 0


class Event(NamedTuple):
    name: str
    event_type: EventType
    roles: Dict[Role, Person]


class Demand(NamedTuple):
    event: Event
    audience: int


class Room(NamedTuple):
    name: str
    capacity: int
    suitability: Iterable[EventType]


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
