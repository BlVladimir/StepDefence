from random import choices, randrange, choice, random

from panda3d.core import Vec2

from scripts.arrays_handlers.arrays_controllers.enemies.enemies_builder import EnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.enemies.movement.group_enemies_builder import GroupEnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.sprite.rect import Rect3D


class EnemiesController:
    """Обработчик врагов"""
    def __init__(self, render:RenderManager, track:Track):
        self._enemies_node = render.main_node3d.attachNewNode('enemy')
        self.__group_enemies_builder = GroupEnemiesBuilder(self._enemies_node, render, track)


    def clear_enemies(self)->None:
        """Удаоляет врагов"""
        self.__group_enemies_builder.clear_enemies()

    def create_enemies(self, wave:int, level:int, tile:Rect3D)->None:
        """Создает врагов"""
        self.__group_enemies_builder.create_enemies(wave, level, tile)

    def move_enemies(self)->None:
        enemies = self._enemies_node.getChildren()

        for i in range(len(enemies)):
            enemies[i].getPythonTag('sprite').external_object.move()