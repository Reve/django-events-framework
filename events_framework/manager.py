import logging
from django.db import transaction

logger = logging.getLogger(__name__)


class EventsManager:
    def __init__(self):
        # (event_model, event_type) -> [handlers]
        self._events_registry = {}

    def register(self, event_model, event_type, handler):
        key = (event_model, event_type)
        handlers = self._events_registry.setdefault(key, [])

        if handler in handlers:
            logger.info("event handler already in registry for %s:%s", event_model.__name__, event_type)
            return

        handlers.append(handler)

    def process(self):
        for (event_model, event_type), handlers in self._events_registry.items():
            events_to_process = event_model.objects.filter(
                type=event_type,
                processed=False,
            )

            for event in events_to_process:
                with transaction.atomic():
                    for e in events_to_process.filter(pk=event.pk).select_for_update(
                        skip_locked=True
                    ):
                        try:
                            for handler in handlers:
                                handler(e)

                            e.processed = True
                            e.save()
                        except Exception as ex:
                            logger.warning("Error processing %s:%s -> %s", event_model.__name__, event_type, ex)
                            e.error = True
                            e.error_message = str(ex)
                            e.processed = True
                            e.save()


manager = EventsManager()
