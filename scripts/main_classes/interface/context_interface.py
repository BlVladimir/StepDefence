from typing import Protocol, runtime_checkable

from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.main_classes.events.event_class import Event
from scripts.main_classes.events.event_handler import EventHandler
from scripts.main_classes.interaction.key_watcher import KeyWatcher
from scripts.main_classes.interaction.render import Render
from scripts.main_classes.settings import Settings
from scripts.scene.scene_controller import SceneController


@runtime_checkable
class IContext(Protocol):
    """Интерфейс контекста"""
    __event_handler:EventHandler
    _scene_controller:SceneController
    _render:Render
    _key_watcher:KeyWatcher
    _settings:Settings
    _buttons_controller:ButtonsController

    def send_event(self, event:Event)->None:
        pass

    @property
    def scene_controller(self)->SceneController:
        pass

    @property
    def render(self)->Render:
        pass

    @property
    def key_watcher(self)->KeyWatcher:
        pass

    @property
    def settings(self)->Settings:
        pass

    @property
    def buttons_controller(self)->ButtonsController:
        pass