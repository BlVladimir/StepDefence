from random import choices, randrange, choice, random
from unittest import TestCase

from scripts.arrays_handlers.arrays_controllers.enemies.enemies_builder import EnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class EnemiesController:
    """Обработчик врагов"""
    def __init__(self, render:RenderManager):
        self.__enemies_builder = EnemiesBuilder(render.main_node3d.attachNewNode('enemies'), render.loader)
        self.__type_tuple = ('basic', 'big', 'armored', 'regen')


    def clear_enemies(self)->None:
        """Удаоляет врагов"""
        self.__enemies_builder.clear_enemies()

    def create_enemy(self, wave:int, level:int, tile:Tile)->None:
        """Создает врагов"""
        for rect in self.__create_rects(tile, randrange(1, 4)):
            self.__enemies_builder.create_enemy(wave, rect, choice(self.__type_tuple[0:level+2] if level < 3 else self.__type_tuple))

    @staticmethod
    def __create_rects(tile:Tile, count:int):
        rects = []
        points = choices(((0, 0), (1, 0), (0, 1), (1, 1)), k=count)
        rect = tile.sprite.rect
        size = min(rect.width, rect.height)
        for y in (0, 1):
            for x in (0, 1):
                if (x, y) in points:
                    rects.append(Rect3D(x=rect.x + 1/6*size*(1+2*x) - 0.25*size + 1/6*size*random(),
                                        y=rect.y + 1/6*size*(1+2*y) - 0.25*size + 1/6*size*random(),
                                        width=0.5*size,
                                        height=0.5*size))
        return rects
