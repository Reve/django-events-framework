import pytest
from events_framework.manager import manager

from .events import PersonEvents
from .models import Person, PersonEvent


def test_register_decorator():
    assert len(manager._events_registry.keys()) == 1

    for handler, props in manager._events_registry.items():
        assert props["type"] == PersonEvents.CREATED
        assert props["event_model"] is PersonEvent
        assert callable(handler)


@pytest.mark.django_db
def test_event_is_being_processed():
    person = Person(name="John")
    person.save()

    manager.process()

    person.refresh_from_db()

    assert PersonEvent.objects.filter(person=person, processed=True).exists()
    assert person.activation_link_sent is True
