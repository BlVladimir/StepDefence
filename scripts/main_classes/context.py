from direct.showbase.ShowBase import ShowBase

from scripts.main_classes.events.event_handler import EventHandler
from scripts.main_classes.render import Render
from scripts.scene.scene_classes.scene_controller import SceneController


class Context:
    """Через этот класс осуществляются все взаимодействия в программе"""
    def __init__(self, render:Render):
        self.__event_handler = EventHandler()
        self.__scene_controller = SceneController()
        self.__render = render