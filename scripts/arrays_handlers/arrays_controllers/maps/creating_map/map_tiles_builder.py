from panda3d.core import NodePath, Loader

from scripts.arrays_handlers.arrays_controllers.maps.creating_map.finder_track import FinderTrack
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.tile_builder import TilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.sprite.rect import Rect3D


class MapTilesBuilder:
    def __init__(self, maps_config:MapsConfig, maps_node:NodePath, loader:Loader):
        self.__maps_config = maps_config
        self.__tiles_builder = TilesBuilder(maps_node, loader)
        self.__finder_track = FinderTrack()
        self._track = Track()

        self._first_tile = None

    def create_map_tiles(self, level):
        """Создает тайлы для карты карту"""
        map_array = self.__maps_config.maps_array[level]
        track = self.__finder_track.find_track(map_array)
        half_x, half_y = 0.5 * len(map_array[0]) * 1.2 - 0.1, 0.5 * len(map_array) * 1.2 - 0.1
        for y in range(len(map_array)):
            for x in range(len(map_array[y])):
                if map_array[y][x] in (1, 2):
                    if (x, y) in track.keys():
                        rect = Rect3D(1.2 * x - half_x, 1.2 * y - half_y - 0.2 * (track[(x, y)] == 1 or track[(x, y)] == 3), 1, 1.2,
                                      (1.2 * x - half_x + 0.5, 1.2 * y - half_y + 0.5))
                        tile = self.__tiles_builder.create_tile(self.__maps_config.keys[map_array[y][x]], rect)
                        tile.sprite.rotate((track[(x, y)]) * 90)
                    else:
                        raise ValueError('(x, y) not in track keys')
                    if map_array[y][x] == 2:
                        self._first_tile = tile
                else:
                    rect = Rect3D(1.2 * x - half_x, 1.2 * y - half_y, 1, 1)
                    if map_array[y][x] in self.__maps_config.keys.keys():
                        self.__tiles_builder.create_tile(self.__maps_config.keys[map_array[y][x]], rect)
        self._track.set_first_tile(self._first_tile)
        self._track.track = track

    def reset_map(self):
        self.__tiles_builder.reset_counter()
        self._first_tile = None

    @property
    def first_tile(self)->Tile:
        return self._first_tile

    @property
    def track(self)->Track:
        return self._track