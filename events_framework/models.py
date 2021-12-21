from django.db import models
from django.db.models.fields.json import JSONField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EventModel(models.Model):
    date = models.DateTimeField(
        _("Date"),
        default=timezone.now,
        editable=False,
    )

    parameters = JSONField(
        _("Parameters"),
        blank=True,
        default=dict,
    )

    processed = models.BooleanField(
        _("Proccesed"),
        default=False,
    )

    class Meta:
        abstract = True
        ordering = ("date",)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.type!r})"
