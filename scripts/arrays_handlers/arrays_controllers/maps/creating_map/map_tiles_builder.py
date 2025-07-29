from panda3d.core import NodePath, Loader

from scripts.arrays_handlers.arrays_controllers.maps.creating_map.finder_track import FinderTrack
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.tile_builder import TilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.sprite.rect import Rect3D


class MapTilesBuilder:
    def __init__(self, maps_config:MapsConfig, maps_node:NodePath, loader:Loader):
        self.__maps_config = maps_config
        self.__tiles_builder = TilesBuilder(maps_node, loader)
        self.__finder_track = FinderTrack()
        self._track = None

    def create_map_tiles(self, level):
        """Создает тайлы для карты карту"""
        map_array = self.__maps_config.maps_array[level]
        self._track = self.__finder_track.find_track(map_array)
        half_x, half_y = 0.5 * len(map_array[0]) * 1.2 - 0.1, 0.5 * len(map_array) * 1.2 - 0.1
        for y in range(len(map_array)):
            for x in range(len(map_array[y])):
                if map_array[y][x] in (1, 2):
                    if (x, y) in self._track.keys():
                        rect = Rect3D(1.2 * x - half_x, 1.2 * y - half_y - 0.2 * (self._track[(x, y)] == 1 or self._track[(x, y)] == 3), 1, 1.2,
                                      (1.2 * x - half_x + 0.5, 1.2 * y - half_y + 0.5))
                        tile = self.__tiles_builder.create_tile(self.__maps_config.keys[map_array[y][x]], rect)
                        tile.sprite.rotate((self._track[(x, y)]) * 90)
                    else:
                        raise ValueError('(x, y) not in track keys')
                else:
                    rect = Rect3D(1.2 * x - half_x, 1.2 * y - half_y, 1, 1)
                    if map_array[y][x] in self.__maps_config.keys.keys():
                        self.__tiles_builder.create_tile(self.__maps_config.keys[map_array[y][x]], rect)

    @property
    def track(self):
        return self._track