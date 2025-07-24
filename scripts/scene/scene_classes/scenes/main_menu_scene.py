from scripts.scene.scene_classes.scenes.abstract_scene import Scene
from scripts.interface.i_main_menu_scene import IMainMenuScene


class MainMenuScene(Scene, IMainMenuScene):
    """Сцена главного меню"""
    @staticmethod
    def name():
        return 'main_menu'