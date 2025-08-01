from panda3d.core import Loader

from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.towers.towers_builder import TowerBuilder
from scripts.arrays_handlers.parts_handler.using_element_controller import UsingElementController
from scripts.main_classes.settings import Settings


class TowersController:
    """Обработчик башен"""
    def __init__(self, loader:Loader, settings:Settings):
        self.__tower_builder = TowerBuilder(loader)
        self._settings = settings

    def create_tower(self, type_tower:str, tile:Tile):
        self.__tower_builder.create_tower(type_tower, tile, self._settings)

    def clear_towers(self):
        self.__tower_builder.reset_counter()