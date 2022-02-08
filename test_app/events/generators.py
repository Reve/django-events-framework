from . import PersonEvents
from ..models import PersonEvent


def created_event(person):
    return PersonEvent.objects.create(
        person=person,
        type=PersonEvents.CREATED,
    )
