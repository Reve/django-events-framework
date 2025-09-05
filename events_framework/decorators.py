from .manager import manager


def register(event_model, event_type):
    def middle(func):
        manager.register(event_model, event_type, func)

        return func

    return middle
