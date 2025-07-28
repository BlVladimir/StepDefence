from logging import warning

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
        self._selected_tile_sprite = None
        self._using_tile_sprite = None

    def create_map_tiles(self, level):
        """Создает тайлы для карты карту"""
        self.__map_tiles_builder.create_map_tiles(level)

    def select_tile(self, tile_sprite:Sprite3D):
        """Выделяет тайл"""
        if self._selected_tile_sprite != tile_sprite:
            if self._selected_tile_sprite is not None and (self._selected_tile_sprite != self._using_tile_sprite):
                self._selected_tile_sprite.is_using = False
            self._selected_tile_sprite = tile_sprite
            tile_sprite.is_using = True

    def unselect_tile(self):
        """Убирает выделение"""
        if self._selected_tile_sprite != self._using_tile_sprite:
            self._selected_tile_sprite.is_using = False
        self._selected_tile_sprite = None

    def using_tile(self):
        """Назначает тайл активным"""
        if not self._using_tile_sprite is None:
            self._using_tile_sprite.is_using = False
        if not self._selected_tile_sprite is None:
            self._using_tile_sprite = self._selected_tile_sprite
            self._using_tile_sprite.is_using = True

    @property
    def track(self):
        return self.__map_tiles_builder.track