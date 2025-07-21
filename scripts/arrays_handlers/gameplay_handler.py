from scripts.arrays_handlers.parts_handler.mediator_controllers import MediatorControllers
from scripts.arrays_handlers.parts_handler.shop import Shop
from scripts.main_classes.DTO.render import Render


class GameplayHandler:
    """Класс, управляющий игрой"""
    def __init__(self, render:Render):
        self.__mediator_controllers = MediatorControllers(render)
        self.__shop = Shop()

    def create_scene(self, level):
        self.__mediator_controllers.create_scene(level)

    def remove_scene(self):
        self.__mediator_controllers.remove_scene()