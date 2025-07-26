from scripts.arrays_handlers.arrays_controllers.enemies.enemies_controller import EnemiesController
from scripts.arrays_handlers.arrays_controllers.maps.maps_controllers import MapsController
from scripts.arrays_handlers.arrays_controllers.towers.towers_controller import TowersController
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.sprite.sprite3D import Sprite3D


class MediatorControllers:
    """Посредник между контроллерами основных классов"""
    def __init__(self, render:RenderManager):
        self.__enemies_controller = EnemiesController()
        self.__towers_controller = TowersController()
        self.__maps_controller = MapsController(render)

    def create_scene(self, level):
        self.__maps_controller.create_map(level)

    def remove_scene(self):
        self.__maps_controller.clear_map()

    def select_element(self, sprite:Sprite3D):
        match sprite.main_node.getName():
            case 'tile':
                self.__maps_controller.select_element(sprite)

    def unselect_element(self, sprite:Sprite3D):
        match sprite.main_node.getName():
            case 'tile':
                self.__maps_controller.unselect_element(sprite)