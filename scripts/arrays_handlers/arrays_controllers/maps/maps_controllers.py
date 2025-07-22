from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tiles_controller import TilesController
from scripts.main_classes.interaction.render import Render


class MapsController:
    """Обработчик карт"""
    def __init__(self, render:Render):
        self.__map_node = render.main_node3d.attachNewNode("empty_node_name")
        self.__tiles_controller = TilesController(self.__map_node, render.loader)
        self.__map_config = MapsConfig()

    def create_map(self, level):
        self.__tiles_controller.create_map(self.__map_config, level)

    def clear_map(self):
        self.__tiles_controller.clear_tiles()