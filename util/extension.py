import hikari
import inspect


def listener(*event_types):
    def decorator(func):
        func.__listener_events__ = event_types
        return func

    return decorator


class Extension:
    async def load(self, client: hikari.GatewayBot):
        for _, method in inspect.getmembers(self, predicate=inspect.ismethod):
            for event_type in getattr(method, "__listener_events__", []):
                client.event_manager.subscribe(event_type, method)

    async def unload(self, client: hikari.GatewayBot):
        for _, method in inspect.getmembers(self, predicate=inspect.ismethod):
            for event_type in getattr(method, "__listener_events__", []):
                client.event_manager.unsubscribe(event_type, method)
