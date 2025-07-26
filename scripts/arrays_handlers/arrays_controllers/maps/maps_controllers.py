from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tiles_controller import TilesController
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.sprite.sprite3D import Sprite3D


class MapsController:
    """Обработчик карт"""
    def __init__(self, render:RenderManager):
        self.__map_node = render.main_node3d.attachNewNode("map_node")
        self.__map_config = MapsConfig()
        self.__tiles_controller = TilesController(self.__map_config, self.__map_node, render.loader)

    def create_map(self, level):
        self.__tiles_controller.create_map_tiles(level)

    def clear_map(self):
        self.__map_node.getChildren().detach()

    def select_element(self, sprite:Sprite3D):
        match sprite.main_node.getName():
            case 'tile':
                self.__tiles_controller.select_tile(sprite)

    def unselect_element(self, sprite:Sprite3D):
        match sprite.main_node.getName():
            case 'tile':
                self.__tiles_controller.unselect_tile(sprite)