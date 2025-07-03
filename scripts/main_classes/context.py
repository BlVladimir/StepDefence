from direct.showbase.ShowBase import ShowBase

from scripts.main_classes.events.event_handler import EventHandler
from scripts.scene.scene_classes.scene_controller import SceneController


class Context:
    def __init__(self, main_class:ShowBase):
        self.__event_handler = EventHandler()
        self.__scene_controller = SceneController()