from events_framework.decorators import register

from . import PersonEvents
from ..models import PersonEvent


@register(PersonEvent, PersonEvents.CREATED)
def handle_object_created(e):
    e.person.activation_link_sent = True
    e.person.save()
