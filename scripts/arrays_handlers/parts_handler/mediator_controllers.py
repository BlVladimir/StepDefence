from scripts.arrays_handlers.arrays_controllers.enemy.enemies_controller import EnemiesController
from scripts.arrays_handlers.arrays_controllers.maps.maps_controllers import MapsController
from scripts.arrays_handlers.arrays_controllers.towers.towers_controller import TowersController


class MediatorControllers:
    """Посредник между контроллерами основных классов"""
    def __init__(self):
        self.__enemies_controller = EnemiesController()
        self.__towers_controller = TowersController()
        self.__maps_controller = MapsController