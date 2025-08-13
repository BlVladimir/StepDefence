from logging import warning, debug
from typing import Any, Callable, Optional


class EventBus:
    _listeners = {}

    @classmethod
    def subscribe(cls, event_type:str, listener:Callable[[str, Optional[Any]], None])->None:
        cls._listeners.setdefault(event_type, []).append(listener)

    @classmethod
    def unsubscribe(cls, event_type:str, listener:Callable[[str, Optional[Any]], None])->None:
        if event_type in cls._listeners:
            cls._listeners[event_type].remove(listener)
        else:
            warning(f'event_type {event_type} not in _listeners')

    @classmethod
    def publish(cls, event_type:str, data:Any=None)->None:
        for listener in cls._listeners.get(event_type, []):
            listener(event_type, data)