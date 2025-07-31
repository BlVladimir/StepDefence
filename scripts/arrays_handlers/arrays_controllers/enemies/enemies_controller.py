from random import choices, randrange, choice, random

from panda3d.core import Vec2

from scripts.arrays_handlers.arrays_controllers.enemies.enemies_builder import EnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.sprite.rect import Rect3D


class EnemiesController:
    """Обработчик врагов"""
    def __init__(self, render:RenderManager, track:Track):
        self._enemies_node = render.main_node3d.attachNewNode('enemies')
        self._track_node = render.main_node3d.attachNewNode('track')
        self.__enemies_builder = EnemiesBuilder(self._enemies_node, render.loader, track, self._track_node)
        self.__type_tuple = ('basic', 'big', 'armored', 'regen')


    def clear_enemies(self)->None:
        """Удаоляет врагов"""
        self.__enemies_builder.clear_enemies()
        self._track_node.getChildren().detach()

    def create_enemy(self, wave:int, level:int, tile:Tile)->None:
        """Создает врагов"""
        rects, poses_on_tile = self.__create_rects(tile, randrange(1, 4))
        try:
            for i in range(len(rects)):
                self.__enemies_builder.create_enemy(wave, rects[i], choice(self.__type_tuple[0:level+2] if level < 3 else self.__type_tuple), poses_on_tile[i])
        except KeyError:
            raise KeyError('len(rects) != len(poses_on_tile)')

    @staticmethod
    def __create_rects(tile:Tile, count:int):
        rects = []
        poses_on_tile = []
        points = choices(((0, 0), (1, 0), (0, 1), (1, 1)), k=count)
        rect = tile.sprite.rect
        size = min(rect.width, rect.height)
        for y in (0, 1):
            for x in (0, 1):
                if (x, y) in points:
                    pos_on_tile = Vec2(1/6*size*(1+3*x), - 1/6*size*(1+3*y))
                    rects.append(Rect3D(top_left=Vec2(rect.x + 1/6*size*random(),
                                        rect.y - 1/6*size*random())+pos_on_tile,
                                        width=0.5*size,
                                        height=0.5*size))
                    poses_on_tile.append(pos_on_tile)
        return rects, poses_on_tile

    def move_enemies(self)->None:
        enemies = self._enemies_node.getChildren()

        for i in range(len(enemies)):
            enemies[i].getPythonTag('sprite').external_object.move()