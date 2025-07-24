from typing import Protocol, runtime_checkable

from scripts.interface.i_button_controller import IButtonsController
from scripts.interface.i_key_watcher import IKeyWatcher
from scripts.interface.i_render import IRender
from scripts.interface.i_scene_controller import ISceneController
from scripts.interface.i_settings import ISettings
from scripts.interface.i_task_manager import ITaskManager
from scripts.main_classes.events.event_class import Event

@runtime_checkable
class IContext(Protocol):
    def send_event(self, event: Event)->None:
        ...
    @property
    def scene_controller(self)->ISceneController:
        ...
    @property
    def render(self)->IRender:
        ...
    @property
    def key_watcher(self)->IKeyWatcher:
        ...
    @property
    def settings(self)->ISettings:
        ...
    @property
    def buttons_controller(self)->IButtonsController:
        ...

    @property
    def taskMgr(self)->ITaskManager:
        ...