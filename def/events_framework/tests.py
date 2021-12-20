from django.db import models

from .decorators import register
from .manager import manager
from .models import EventModel
from .utils import AbstractEvents


class TestEvents(AbstractEvents):
    TEST_EVENT = "test_event"
    CHOICES = [(TEST_EVENT, "This is a test event")]


class TestEvent(EventModel):
    type = models.CharField(
        max_length=255,
        choices=TestEvents.as_choices(),
    )


def test_register_decorator():
    @register(event_model=TestEvent, event_type=TestEvents.TEST_EVENT)
    def handler(e):
        pass

    assert len(manager._events_registry.keys()) == 1
    assert manager._events_registry[TestEvent]["type"] == TestEvents.TEST_EVENT
    assert manager._events_registry[TestEvent]["handler"] is not None
    assert callable(manager._events_registry[TestEvent]["handler"])
