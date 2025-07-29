from panda3d.core import Loader

from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.towers.towers_builder import TowerBuilder


class TowersController:
    """Обработчик башен"""
    def __init__(self, loader:Loader):
        self.__tower_builder = TowerBuilder(loader)

    def create_tower(self, type_tower:str, tile:Tile):
        self.__tower_builder.create_tower(type_tower, tile)

    def clear_towers(self):
        self.__tower_builder.reset_counter()