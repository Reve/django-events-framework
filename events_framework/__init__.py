import logging
from importlib import import_module

import django
from django.conf import settings

logger = logging.getLogger(__name__)


def autodiscover():
    if not hasattr(settings, "EVENT_APPS"):
        return

    if not isinstance(settings.EVENT_APPS, list):
        raise Exception("EVENT_APPS should be a list")

    for app in settings.EVENT_APPS:
        # load processors
        module_path = f"{app}.events.processors"
        try:
            import_module(module_path)
        except ImportError:
            # App may not define processors; that's fine
            continue
        except Exception:
            logger.exception("Error importing %s", module_path)


# backwards compatibility with Django 2.*
if django.VERSION < (3, 2):
    default_app_config = "events_framework.apps.EventsManagerConfig"
