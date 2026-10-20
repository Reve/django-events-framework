import pytest
from events_framework.exceptions import RetryEvent
from events_framework.manager import EventsManager, manager

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


@pytest.mark.django_db
def test_retry_rolls_back_handlers_and_completes_on_a_later_run():
    person = Person(name="John")
    person.save()
    event = PersonEvent.objects.create(person=person, type="publish", parameters={"invoice_id": 42})
    processor = EventsManager()
    calls = []

    def prepare(e):
        calls.append("prepare")
        Person.objects.filter(pk=e.person_id).update(activation_link_sent=True)
        e.parameters["prepared"] = True
        e.save(update_fields=["parameters"])

    def publish(e):
        calls.append("publish")
        if calls.count("publish") == 1:
            raise RetryEvent("Receiver unavailable")

    processor.register(PersonEvent, "publish", prepare)
    processor.register(PersonEvent, "publish", publish)

    processor.process()

    person.refresh_from_db()
    event.refresh_from_db()
    assert calls == ["prepare", "publish"]
    assert person.activation_link_sent is False
    assert event.parameters == {"invoice_id": 42}
    assert event.processed is False
    assert event.error is True
    assert event.error_message == "Receiver unavailable"

    processor.process()

    person.refresh_from_db()
    event.refresh_from_db()
    assert calls == ["prepare", "publish", "prepare", "publish"]
    assert person.activation_link_sent is True
    assert event.parameters == {"invoice_id": 42, "prepared": True}
    assert event.processed is True
    assert event.error is False
    assert event.error_message is None


@pytest.mark.django_db
def test_database_failure_rolls_back_handler_and_records_terminal_error():
    person = Person(name="John")
    person.save()
    event = PersonEvent.objects.create(person=person, type="publish")
    processor = EventsManager()

    def publish(e):
        Person.objects.filter(pk=e.person_id).update(activation_link_sent=True)
        PersonEvent.objects.create(pk=e.pk, person_id=e.person_id, type="publish")

    processor.register(PersonEvent, "publish", publish)
    processor.process()

    person.refresh_from_db()
    event.refresh_from_db()
    assert person.activation_link_sent is False
    assert event.processed is True
    assert event.error is True
    assert event.error_message
