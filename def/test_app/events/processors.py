from events_framework.decorators import register

from . import TestObjectEvents
from ..models import TestEvent

print("*****here")


@register(TestEvent, TestObjectEvents.CREATED)
def handle_object_created(e):
    print(e)
