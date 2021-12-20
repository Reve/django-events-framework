from events_framework.manager import manager

from .events import PersonEvents
from .models import Person


def test_register_decorator():
    assert len(manager._events_registry.keys()) == 1
    assert manager._events_registry[Person]["type"] == PersonEvents.CREATED
    assert manager._events_registry[Person]["handler"] is not None
    assert callable(manager._events_registry[Person]["handler"])
