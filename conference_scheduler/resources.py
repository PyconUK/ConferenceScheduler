from typing import NamedTuple, Sequence, Dict, Iterable, List
from datetime import datetime


class EventType(NamedTuple):
    name: str


class Role(NamedTuple):
    name: str


CHAIR = Role(name='chair')


class Person(NamedTuple):
    name: str
    max_chair_sessions: int = 0


class Room(NamedTuple):
    name: str
    capacity: int
    suitability: Iterable[EventType]


class Slot(NamedTuple):
    room: Room
    starts_at: datetime
    duration: int


class Event(NamedTuple):
    name: str
    event_type: EventType
    duration: int
    roles: Dict[Role, Person]
    tags: List[str]
    unavailability: List


class Demand(NamedTuple):
    event: Event
    audience: int


class ScheduledItem(NamedTuple):
    event: Event
    slot: Slot


class Session(NamedTuple):
    slots: Sequence[Slot]


class Unavailability(NamedTuple):
    person: Person
    slot: Slot


class Shape(NamedTuple):
    """Represents the shape of a 2 dimensional array of events and slots"""
    events: int
    slots: int


class Constraint(NamedTuple):
    label: str
    condition: bool
