from scripts.arrays_handlers.parts_handler.mediator_controllers import MediatorControllers
from scripts.arrays_handlers.parts_handler.shop import Shop


class GameplayHandler:
    """Класс, управляющий игрой"""
    def __init__(self):
        self.__mediator_controllers = MediatorControllers()
        self.__shop = Shop()