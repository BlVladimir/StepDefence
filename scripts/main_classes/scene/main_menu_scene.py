from scripts.main_classes.gui.main_menu_buttons_controller import MainMenuButtonsController
from scripts.main_classes.scene.scene import Scene
from scripts.sprite.sprites_factory import SpritesFactory


class MainMenuScene(Scene):
    def __init__(self, sprites_factory:SpritesFactory):
        super().__init__(sprites_factory, 'main_menu')

        self.__buttons_controller = MainMenuButtonsController(sprites_factory.relationship, self._buttons_node)