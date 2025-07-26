from scripts.arrays_handlers.parts_handler.mediator_controllers import MediatorControllers
from scripts.arrays_handlers.parts_handler.shop import Shop
from scripts.main_classes.interaction.render_manager import RenderManager


class GameplayHandler:
    """Класс, управляющий игрой"""
    def __init__(self, render:RenderManager):
        self._mediator_controllers = MediatorControllers(render)
        self.__shop = Shop()

    def create_scene(self, level):
        self._mediator_controllers.create_scene(level)

    def remove_scene(self):
        self._mediator_controllers.remove_scene()

    @property
    def mediator_controllers(self):
        return self._mediator_controllers