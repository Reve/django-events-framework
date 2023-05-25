import pytest
from events_framework.manager import manager

from .events import PersonEvents
from .models import Person, PersonEvent


def test_register_decorator():
    assert len(manager._events_registry.keys()) == 2


@pytest.mark.django_db
def test_event_is_being_processed():
    person = Person(name="John")
    person.save()

    manager.process()

    person.refresh_from_db()

    assert PersonEvent.objects.filter(person=person, processed=True).exists()
    assert person.activation_link_sent is True


@pytest.mark.django_db
def test_event_fails_error_is_registered():
    person = Person(name="John")
    person.save()
    person.fail()

    manager.process()

    person.refresh_from_db()

    evt  = PersonEvent.objects.get(person=person, error=True)

    assert evt is not None
    assert evt.processed == True
    assert evt.error_message == "This event failed intentionally"

