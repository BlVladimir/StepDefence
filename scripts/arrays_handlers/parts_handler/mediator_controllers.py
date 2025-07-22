from scripts.arrays_handlers.arrays_controllers.enemies.enemies_controller import EnemiesController
from scripts.arrays_handlers.arrays_controllers.maps.maps_controllers import MapsController
from scripts.arrays_handlers.arrays_controllers.towers.towers_controller import TowersController
from scripts.main_classes.interaction.render import Render


class MediatorControllers:
    """Посредник между контроллерами основных классов"""
    def __init__(self, render:Render):
        self.__enemies_controller = EnemiesController()
        self.__towers_controller = TowersController()
        self.__maps_controller = MapsController(render)

    def create_scene(self, level):
        self.__maps_controller.create_map(level)

    def remove_scene(self):
        self.__maps_controller.clear_map()