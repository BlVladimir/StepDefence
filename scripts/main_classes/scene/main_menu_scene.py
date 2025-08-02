from scripts.main_classes.buttons.main_menu_buttons_controller import MainMenuButtonsController
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.scene.scene import Scene


class MainMenuScene(Scene):
    def __init__(self, render_manager:RenderManager):
        super().__init__(render_manager, 'main_menu')

        self.__buttons_controller = MainMenuButtonsController(render_manager.win, self._buttons_node)