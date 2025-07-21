from panda3d.core import PandaNode

from scripts.arrays_handlers.arrays_controllers.maps.finder_track import FinderTrack
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tiles_builder import TilesBuilder
from scripts.sprite.rect import Rect3D


class TilesController:
    """Содержит группу всех тайлов"""
    def __init__(self, maps_node:PandaNode, loader):
        self.__track = []
        self.__tiles_builder = TilesBuilder(maps_node, loader)
        self.__tiles_array = []
        self.__finder_track = FinderTrack()

    def create_map(self, maps_config:MapsConfig, level):
        """Создает карту"""
        map_array = maps_config.maps_array[level]
        self.__track = self.__finder_track.find_track(map_array)
        len_x, len_y = len(map_array[0]), len(map_array)
        half_x, half_y = 0.5*len_x*1.2 - 0.1, 0.5*len_y*1.2 - 0.1
        for y in range(len(map_array)):
            for x in range(len(map_array[y])):
                if map_array[y][x] in (1, 2):
                    if (x, y) in self.__track.keys():
                        rect = Rect3D(1.2 * x - half_x, 1.2 * y - half_y - 0.2*(self.__track[(x, y)] == 2 or self.__track[(x, y)] == 0), 1, 1.2,
                                      (1.2 * x - half_x + 0.5, 1.2 * y - half_y + 0.5))
                        self.__tiles_array.append(self.__tiles_builder.create_tile(maps_config.keys[map_array[y][x]], rect))
                        self.__tiles_array[len(self.__tiles_array)-1].sprite.rotate((self.__track[(x, y)] + 1)*90)
                    else:
                        raise ValueError('(x, y) not in track keys')
                else:
                    rect = Rect3D(1.2*x - half_x, 1.2*y - half_y, 1, 1)
                    if map_array[y][x] in maps_config.keys.keys():
                        self.__tiles_array.append(self.__tiles_builder.create_tile(maps_config.keys[map_array[y][x]], rect))
