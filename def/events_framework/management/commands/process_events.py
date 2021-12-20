from django.core.management import BaseCommand

from ...manager import manager


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(manager._events_registry)
        manager.process()
