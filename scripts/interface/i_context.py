from typing import Protocol, runtime_checkable
from scripts.main_classes.events.event_class import Event

@runtime_checkable
class IContext(Protocol):
    def send_event(self, event: Event):
        ...
    @property
    def scene_controller(self):
        ...
    @property
    def render(self):
        ...
    @property
    def key_watcher(self):
        ...
    @property
    def settings(self):
        ...
    @property
    def buttons_controller(self):
        ... 