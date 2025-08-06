from scripts.arrays_handlers.mediator_controllers import MediatorControllers
from scripts.main_classes.buttons.gameplay_buttons_controller import GameplayButtonsController
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.main_classes.scene.scene import Scene
from scripts.sprite.sprites_factory import SpritesFactory


class GameplayScene(Scene):
    def __init__(self, sprites_factory:SpritesFactory):
        super().__init__(sprites_factory, 'gameplay')
        self.__buttons_controller = GameplayButtonsController(sprites_factory.relationship, self._buttons_node)
        self.__mediator_controllers = MediatorControllers(self._scene_node, sprites_factory)
        self._level = 0

    def hide(self)->None:
        """Скрывает сцену"""
        super().hide()
        self.__mediator_controllers.remove_scene()

    def show(self)->None:
        super().show()
        self.__mediator_controllers.create_scene(self._level)

    @property
    def level(self)->int:
        return self._level

    @level.setter
    def level(self, value:int):
        self._level = value