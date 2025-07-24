from typing import Protocol, runtime_checkable
from scripts.main_classes.events.event_class import Event

@runtime_checkable
class IEventHandler(Protocol):
    @staticmethod
    def handle_event(event: Event, context):
        ... 