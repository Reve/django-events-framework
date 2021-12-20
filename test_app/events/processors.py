from events_framework.decorators import register

from . import PersonEvents
from ..models import Person


@register(Person, PersonEvents.CREATED)
def handle_object_created(e):
    print(e)
