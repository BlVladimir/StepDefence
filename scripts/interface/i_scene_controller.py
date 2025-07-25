from typing import Protocol, runtime_checkable

from scripts.interface.i_context import IContext
from scripts.main_classes.events.event_class import Event

@runtime_checkable
class ISceneController(Protocol):
    def change_scene(self, event: Event, context:IContext)->None:
        ...
    def get_name_current_scene(self)->str:
        ...