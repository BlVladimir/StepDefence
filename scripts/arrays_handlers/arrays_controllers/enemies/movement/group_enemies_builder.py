from random import randrange, choice, choices, random

from panda3d.core import NodePath, Vec2

from scripts.arrays_handlers.arrays_controllers.enemies.enemies_builder import EnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprites_factory import SpritesFactory


class GroupEnemiesBuilder:
    """Создает группу врагов"""
    def __init__(self, enemies_node:NodePath, sprites_factory:SpritesFactory, track:Track):
        self._enemies_node = enemies_node
        self.__enemies_builder = EnemiesBuilder(self._enemies_node, sprites_factory, track)
        self.__type_tuple = ('basic', 'big', 'armored', 'regen')

    def clear_enemies(self)->None:
        """Удаоляет врагов"""
        self._enemies_node.getChildren().detach()

    def create_enemies(self, wave:int, level:int, tile:Rect3D)->None:
        """Создает врагов"""
        rects, poses_on_tile, started_divisiones = self.__create_rects(tile, randrange(1, 4))
        try:
            for i in range(len(rects)):
                self.__enemies_builder.create_enemy(wave, rects[i], choice(self.__type_tuple[0:level+2] if level < 3 else self.__type_tuple), poses_on_tile[i], started_divisiones[i])
        except KeyError:
            raise KeyError('len(rects) != len(poses_on_tile)')

    @staticmethod
    def __create_rects(rect:Rect3D, count:int):
        rects = []
        poses_on_tile = []
        started_divisiones = []
        points = choices(((0, 0), (1, 0), (0, 1), (1, 1)), k=count)
        size = rect.width
        for y in (0, 1):
            for x in (0, 1):
                if (x, y) in points:
                    pos_on_tile = Vec2(1/6*size*(1+3*x), - 1/6*size*(1+3*y))
                    started_division = Vec2(1/6*size*random(), -1/6*size*random())
                    rects.append(Rect3D(top_left=Vec2(rect.x, rect.y) + started_division + pos_on_tile + Vec2(-0.25*size, 0.25*size),
                                        width=0.5*size,
                                        height=0.5*size))
                    poses_on_tile.append(pos_on_tile)
                    started_divisiones.append(started_division)
        return rects, poses_on_tile, started_divisiones

