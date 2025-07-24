from typing import Protocol, runtime_checkable
from scripts.main_classes.events.event_class import Event

@runtime_checkable
class ISceneController(Protocol):
    def change_scene(self, event: Event):
        ...
    def get_name_current_scene(self):
        ... 