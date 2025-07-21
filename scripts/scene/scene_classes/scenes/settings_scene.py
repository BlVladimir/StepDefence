from scripts.main_classes.DTO.render import Render
from scripts.scene.buttons.buttons_controller import ButtonsController, NullButtonsController
from scripts.scene.scene_classes.scenes.abstract_scene import Scene


class SettingsScene(Scene):
    """Сцена настроек"""
    def __init__(self, render:Render):
        super().__init__(render)
        self.__button_controller = NullButtonsController(render)