from events_framework.utils import AbstractEvents


class PersonEvents(AbstractEvents):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"

    CHOICES = [
        (CREATED, "Test object was created"),
        (UPDATED, "Test object was updated"),
        (DELETED, "Test object was deleted"),
    ]
