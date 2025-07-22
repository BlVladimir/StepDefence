from scripts.arrays_handlers.gameplay_handler import GameplayHandler
from scripts.main_classes.interaction.render import Render
from scripts.scene.scene_classes.scenes.abstract_scene import Scene


class GameplayScene(Scene):
    """Сцена во время игры"""
    def __init__(self, render:Render):
        self.__gameplay_handler = GameplayHandler(render)

    def create_scene(self, level):
        self.__gameplay_handler.create_scene(level)

    def close_scene(self):
        self.__gameplay_handler.remove_scene()

    @staticmethod
    def name():
        return 'gameplay'