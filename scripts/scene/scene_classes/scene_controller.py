from scripts.scene.scene_classes.scenes.gameplay_scene import GameplayScene
from scripts.scene.scene_classes.scenes.main_menu_scene import MainMenuScene
from scripts.scene.scene_classes.scenes.settings_scene import SettingsScene


class SceneController:
    """Класс, обрабатывающий сцены"""
    def __init__(self):
        self.__gameplay_scene = GameplayScene()
        self.__settings_scene = SettingsScene()
        self.__main_menu_scene = MainMenuScene()