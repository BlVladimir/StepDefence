from scripts.main_classes.interaction.key_watcher import KeyWatcher
from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.main_classes.events.event_class import Event
from scripts.main_classes.events.event_handler import EventHandler
from scripts.main_classes.interaction.render import Render
from scripts.main_classes.settings import Settings
from scripts.scene.scene_controller import SceneController


class Context:
    """Через этот класс осуществляются все взаимодействия в программе"""
    def __init__(self, render:Render, key_watcher:KeyWatcher):
        self.__event_handler = EventHandler()
        self._scene_controller = SceneController(render)
        self._render = render
        self._key_watcher = key_watcher
        self._settings = Settings()
        self._buttons_controller = ButtonsController(self._render)
        self.__s = 2

    def send_event(self, event:Event):
        """Отправляет event на обработку"""
        if type(event) == Event:
            self.__event_handler.handle_event(event, self)

    @property
    def scene_controller(self):
        return self._scene_controller

    @property
    def render(self):
        return self._render

    @property
    def key_watcher(self):
        return self._key_watcher

    @property
    def settings(self):
        return self._settings

    @property
    def buttons_controller(self):
        return self._buttons_controller