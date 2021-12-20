from . import TestObjectEvents
from ..models import TestObjectEvent


def created_event(test_object):
    return TestObjectEvent.object.create(
        test_object=test_object,
        type=TestObjectEvents.CREATED,
    )
