from django.db import models

from events_framework.models import EventModel
from .events import PersonEvents


class Person(models.Model):
    name = models.CharField(max_length=64)
    activation_link_sent = models.BooleanField(default=False)

    def save(self) -> None:
        from .events import generators as events

        super().save()
        events.created_event(self)

    def fail(self) -> None:
        from .events import generators as events

        events.failed_event(self)


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
