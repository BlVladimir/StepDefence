from scripts.arrays_handlers.gameplay_handler import GameplayHandler
from scripts.interface.i_context import IContext
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.scene.scene_classes.scenes.abstract_scene import Scene
from scripts.interface.i_gameplay_scene import IGameplayScene


class GameplayScene(Scene, IGameplayScene):
    """Сцена во время игры"""
    def __init__(self, render:RenderManager, context:IContext):
        self._gameplay_handler = GameplayHandler(render, context)

    def create_scene(self, level):
        self._gameplay_handler.create_scene(level)

    def close_scene(self):
        self._gameplay_handler.remove_scene()

    @staticmethod
    def name():
        return 'gameplay'

    @property
    def gameplay_handler(self):
        return self._gameplay_handler