from scripts.scene.buttons.battuns_controller import ButtonsController
from scripts.scene.scene_classes.scenes.abstract_scene import Scene


class SettingsScene(Scene):
    """Сцена настроек"""
    def __init__(self):
        super().__init__()
        self.__button_controller = ButtonsController()