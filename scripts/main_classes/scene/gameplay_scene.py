from scripts.arrays_handlers.mediator_controllers import MediatorControllers
from scripts.main_classes.buttons.gameplay_buttons_controller import GameplayButtonsController
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.scene.scene import Scene


class GameplayScene(Scene):
    def __init__(self, render_manager:RenderManager, context:'Context'):
        super().__init__(render_manager, 'gameplay')
        self.__buttons_controller = GameplayButtonsController(render_manager.win, self._buttons_node)
        self.__mediator_controllers = MediatorControllers(self._scene_node, render_manager.loader, context, context.settings)
        self._level = 0

        EventBus.subscribe('open_shop', lambda event_type, data: self.__buttons_controller.open_shop())
        EventBus.subscribe('close_shop', lambda event_type, data: self.__buttons_controller.close_shop())

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