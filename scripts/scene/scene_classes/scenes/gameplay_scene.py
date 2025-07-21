from scripts.arrays_handlers.gameplay_handler import GameplayHandler
from scripts.main_classes.DTO.render import Render
from scripts.scene.buttons.buttons_controller import ButtonsController, NullButtonsController
from scripts.scene.scene_classes.scenes.abstract_scene import Scene


class GameplayScene(Scene):
    """Сцена во время игры"""
    def __init__(self, render:Render):
        super().__init__(render)
        self.__button_controller = NullButtonsController(render)
        self.__gameplay_handler = GameplayHandler(render)

    def create_scene(self, level):
        self.__gameplay_handler.create_scene(level)