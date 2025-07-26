from panda3d.core import PandaNode

from scripts.arrays_handlers.arrays_controllers.maps.creating_map.finder_track import FinderTrack
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.map_tiles_builder import MapTilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.tile_builder import TilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class TilesController:
    """Содержит группу всех тайлов"""
    def __init__(self, maps_config:MapsConfig, maps_node:PandaNode, loader):
        self.__map_tiles_builder = MapTilesBuilder(maps_config, maps_node, loader)
        self._selected_tile = None

    def create_map_tiles(self, level):
        """Создает тайлы для карты карту"""
        self.__map_tiles_builder.create_map_tiles(level)

    def select_tile(self, tile:Sprite3D):
        if self._selected_tile is None:
            self._selected_tile = tile
            tile.add_wireframe()
        elif not self._selected_tile == tile:
            self._selected_tile.delete_wireframe()
            self._selected_tile = tile
            tile.add_wireframe()

    def unselect_tile(self, tile:Sprite3D):
        self._selected_tile.delete_wireframe()
        self._selected_tile = None

    @property
    def track(self):
        return self.__map_tiles_builder.track