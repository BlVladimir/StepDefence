from scripts.main_classes.DTO.render import Render
from scripts.scene.buttons.buttons_controller import ButtonsController
from scripts.scene.scene_classes.scenes.abstract_scene import Scene


class MainMenuScene(Scene):
    """Сцена главного меню"""
    def __init__(self, render:Render):
        super().__init__(render)
        self.__button_controller = ButtonsController(render)

    def hide(self):
        self.__button_controller.remove_button()

    def action(self, context):
        return self.__button_controller.action(context)