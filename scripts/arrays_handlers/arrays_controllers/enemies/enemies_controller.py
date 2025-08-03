from __future__ import annotations

from panda3d.core import NodePath

from scripts.arrays_handlers.arrays_controllers.enemies.movement.group_enemies_builder import GroupEnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.arrays_handlers.using_element_controller import UsingElementController
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D
from scripts.sprite.sprites_factory import SpritesFactory


class EnemiesController:
    """Обработчик врагов"""
    def __init__(self, scene_gameplay_node:NodePath, sprites_factory:SpritesFactory, track:Track):
        self._enemies_node = scene_gameplay_node.attachNewNode('enemy')
        self._track_node = scene_gameplay_node.attachNewNode('track')
        self.__group_enemies_builder = GroupEnemiesBuilder(self._enemies_node, self._track_node, sprites_factory, track)

        self.__enemies_selector = UsingElementController()

        EventBus.subscribe('next_round', lambda event_type, data: self.__move_enemies())


    def clear_enemies(self)->None:
        """Удаоляет врагов"""
        self.__group_enemies_builder.clear_enemies()

    def create_enemies(self, wave:int, level:int, tile:Rect3D)->None:
        """Создает врагов"""
        self.__group_enemies_builder.create_enemies(wave, level, tile)

    def __move_enemies(self)->None:
        enemies = self._enemies_node.getChildren()

        for i in range(len(enemies)):
            enemies[i].getPythonTag('sprite').external_object.move()

    def handle_enemy_action(self, action: str, enemy:Sprite3D = None) -> None:
        """Обрабатывает действия с врагами"""
        match action:
            case 'select':
                self.__enemies_selector.select_sprite(enemy)
            case 'unselect':
                self.__enemies_selector.unselect_sprite()
            case 'using':
                self.__enemies_selector.using_sprite()