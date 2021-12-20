from django.db import models

from events_framework.models import EventModel
from .events import PersonEvents


class Person(models.Model):
    name = models.CharField(max_length=64)

    def save(self) -> None:
        from .events import generators as events

        events.created_event(self)
        return super().save()


class PersonEvent(EventModel):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="events",
    )

    type = models.CharField(
        max_length=128,
        choices=PersonEvents.as_choices(),
    )
