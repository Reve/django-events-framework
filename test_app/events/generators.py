from . import PersonEvents
from ..models import PersonEvent


def created_event(test_object):
    return PersonEvent.object.create(
        test_object=test_object,
        type=PersonEvents.CREATED,
    )
