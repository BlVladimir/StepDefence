from scripts.main_classes.DTO.key_watcher import KeyWatcher
from scripts.main_classes.events.event_class import Event
from scripts.main_classes.events.event_handler import EventHandler
from scripts.main_classes.DTO.render import Render
from scripts.main_classes.settings import Settings
from scripts.scene.scene_controller import SceneController


class Context:
    """Через этот класс осуществляются все взаимодействия в программе"""
    def __init__(self, render:Render, key_watcher:KeyWatcher):
        self.__event_handler = EventHandler()
        self.__scene_controller = SceneController()
        self.__render = render
        self.__key_watcher = key_watcher
        self.__settings = Settings()

    def send_event(self, event:Event):
        """Отправляет event на обработку"""
        self.__event_handler.handle_event(event, self)

    @property
    def scene_controller(self):
        return self.__scene_controller

    @property
    def render(self):
        return self.__render

    @property
    def key_watcher(self):
        return self.__key_watcher

    @property
    def settings(self):
        return self.__settings