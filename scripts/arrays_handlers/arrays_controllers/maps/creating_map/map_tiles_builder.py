from logging import error

import yaml
from panda3d.core import NodePath, Vec2

from scripts.arrays_handlers.arrays_controllers.maps.creating_map.finder_track import FinderTrack
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.tile_builder import TilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprites_factory import SpritesFactory


class MapTilesBuilder:
    def __init__(self, maps_node:NodePath, sprites_factory:SpritesFactory):
        self.__finder_track = FinderTrack()
        self._track = Track()

        self._first_tile_rect = None

        try:
            with open('configs/maps_config.yaml', 'r') as file:
                maps_config = yaml.safe_load(file)
            self.__conf = MapsConfig(**maps_config)
        except Exception as Er:
            raise ValueError(Er)

        self.__tiles_builder = TilesBuilder(maps_node, sprites_factory, self.__conf)

    def create_map_tiles(self, level: int):
        """Создает тайлы для карты карту"""
        map_array = self.__conf.get_map(level)
        track = self.__finder_track.find_track(map_array)
        half_x, half_y = 0.5 * len(map_array[0]) * 1.2 - 0.1, 0.5 * len(map_array) * 1.2 - 0.1
        for y in range(len(map_array)):
            for x in range(len(map_array[y])):
                if map_array[y][x] in (1, 2):
                    try:
                        rect = Rect3D(Vec2(1.2 * x - half_x, - 1.2 * y + half_y + 0.2), 1, 1.2,
                                      Vec2(1.2 * x - half_x + 0.5, - 1.2 * y + half_y - 0.5))
                        tile = self.__tiles_builder.create_tile(self.__conf.get_tile(map_array[y][x]), rect)
                        tile.sprite.rotate(-(track[(x, y)]) * 90)
                    except KeyError:
                        error(f'key: {(x, y)}, track: {track}')
                        raise KeyError('(x, y) not in track keys')
                    if map_array[y][x] == 2:
                        self._first_tile_rect = Rect3D(Vec2(1.2 * x - half_x, - 1.2 * y + half_y), 1, 1)
                else:
                    rect = Rect3D(Vec2(1.2 * x - half_x, - 1.2 * y + half_y), 1, 1, Vec2(1.2 * x - half_x + 0.5, - 1.2 * y + half_y - 0.5))
                    if map_array[y][x] in self.__conf.get_all_keys():
                        self.__tiles_builder.create_tile(self.__conf.get_tile(map_array[y][x]), rect)
        self._track.set_first_tile(self._first_tile_rect)
        self._track.set_track(list(track.values()))

    def reset_map(self)->None:
        """Удаляет карту"""
        self.__tiles_builder.reset_counter()
        self._first_tile_rect = None

    @property
    def first_tile_rect(self)->Rect3D:
        return self._first_tile_rect

    @property
    def track(self)->Track:
        return self._track
