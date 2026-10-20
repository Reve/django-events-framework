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
- Multiple handlers: All registered handlers for an `(EventModel, type)` run for each event. If any handler raises, their database changes are rolled back and the event records `error=True` and `error_message`.
- Idempotency: Handlers should be idempotent, as retries or alternative processors may be added later.
- Retries: Ordinary exceptions mark the event as processed. Raise `events_framework.exceptions.RetryEvent` to leave it pending for the next `process_events` invocation. A successful retry clears the error fields. Each retry runs all handlers again, so external operations must tolerate repeated delivery.
- Backoff: Processing makes one attempt per pending event per invocation. The command schedule controls the retry interval; there is no automatic retry limit or exponential backoff.

For a publisher, raise `RetryEvent` when the receiver cannot durably accept the event. Use the same event identity and immutable payload on every delivery attempt. Handlers run inside a database transaction, so use bounded network timeouts and acknowledge processing only after the receiver confirms durable acceptance:

```python
from events_framework.decorators import register
from events_framework.exceptions import RetryEvent


@register(InvoiceEvent, InvoiceEvents.CHANGED)
def publish_invoice_change(event):
    try:
        publish(event.parameters)
    except ReceiverUnavailable as error:
        raise RetryEvent("Invoice event receiver unavailable") from error
```

`publish` and `ReceiverUnavailable` are supplied by the application. Create the event and its immutable payload in the same transaction as the business change. A receiver may accept an event before the sender fails to record success; the receiver must deduplicate repeated deliveries.

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
