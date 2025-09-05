# Overview

An events framework that allows for logging and processing of Django models custom events.

See `CHANGELOG.md` for release notes.

# Setup

## Requirements

- Python 3.6+

## Installation

Install it directly into an activated virtual environment:

```text
$ pip install django-events-framework
```

# Usage

After installation, the framework can be used by:

```text
INSTALLED_APPS = [
    ...,
    "events_framework"
]
```

## Concurrency & Error Handling

- Concurrency: Processing uses database row locks via `select_for_update(skip_locked=True)` to avoid double-processing across workers. Multiple workers can safely call the `process_events` command.
- Multiple handlers: All registered handlers for an `(EventModel, type)` run for each event. If any handler raises, the event is marked as processed with `error=True` and `error_message` set.
- Idempotency: Handlers should be idempotent, as retries or alternative processors may be added later.
- Backoff/retries: The baseline behavior marks failed events as processed to avoid busy loops. Implement custom retry logic by clearing `processed` on failed events or adding a retry counter field in your subclass if needed.

Tested combinations include Django 2.2, 3.2, and 4.2 on supported Python versions.

## Quickstart

1) Declare your events and model

```python
# myapp/events.py
from events_framework.utils import AbstractEvents


class OrderEvents(AbstractEvents):
    CREATED = "created"
    FAILED = "failed"

    CHOICES = [
        (CREATED, "Order was created"),
        (FAILED, "Order processing failed"),
    ]

# myapp/models.py
from django.db import models
from events_framework.models import EventModel
from .events import OrderEvents


class Order(models.Model):
    number = models.CharField(max_length=32)


class OrderEvent(EventModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="events")
    type = models.CharField(max_length=128, choices=OrderEvents.as_choices())
```

2) Generate events in your app logic

```python
# myapp/events/generators.py
from .events import OrderEvents
from ..models import OrderEvent


def created(order):
    return OrderEvent.objects.create(order=order, type=OrderEvents.CREATED)
```

3) Register processors with a decorator

```python
# myapp/events/processors.py
from events_framework.decorators import register
from .events import OrderEvents
from ..models import OrderEvent


@register(OrderEvent, OrderEvents.CREATED)
def on_order_created(event):
    # do something with event.order
    ...
```

4) Enable auto-discovery of processors and run the worker

```python
# settings.py
INSTALLED_APPS = [
    ...,
    "events_framework",
    "myapp",
]

EVENT_APPS = ["myapp"]  # looks for myapp.events.processors
```

Run the processor:

```bash
python manage.py process_events
```
