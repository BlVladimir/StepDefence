from __future__ import annotations

import asyncio
from typing import Set

from panda3d.core import NodePath

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.enemies.group_enemies_builder import GroupEnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.arrays_handlers.arrays_controllers.selector.enemy_selector.enemy_selector import EnemySelector
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D
from scripts.sprite.sprites_factory import SpritesFactory


class EnemiesController:
    """Обработчик врагов"""
    def __init__(self, scene_gameplay_node:NodePath, sprites_factory:SpritesFactory, track:Track, mediator_controllers: 'MediatorControllers'):
        self._enemies_node = scene_gameplay_node.attachNewNode('enemy')
        self.__group_enemies_builder = GroupEnemiesBuilder(self._enemies_node, sprites_factory, track)

        self.__enemies_selector = EnemySelector(lambda :self.get_enemies_set())
        self.__mediator_controller = mediator_controllers
        self.__is_round_ended = False

        EventBus.subscribe('enter_click', lambda event_type, data: self.__round_ended())
        EventBus.subscribe('start_end_turn', lambda event_type, data: EventBus.publish('add_async_task', self.__move_enemies()))

    def clear_enemies(self)->None:
        """Удаоляет врагов"""
        self.__group_enemies_builder.clear_enemies()

    def create_enemies(self, wave:int, level:int, tile:Rect3D)->None:
        """Создает врагов"""
        self.__group_enemies_builder.create_enemies(wave, level, tile)

    async def __move_enemies(self)->None:
        for enemy in self._enemies_node.getChildren():
            enemy.getPythonTag('sprite').external_object.end_turn()
        await asyncio.sleep(1)
        EventBus.publish('complete_end_turn')
        self.__is_round_ended = False

    def handle_enemy_action(self, action: str, enemy_sprite:Sprite3D = None) -> None:
        """Обрабатывает действия с врагами"""
        match action:
            case 'select':
                self.__enemies_selector.select_sprite(enemy_sprite)
            case 'unselect':
                self.__enemies_selector.unselect_sprite()
            case 'using':
                self.__enemies_selector.set_used_sprite()

    def get_enemies_set(self)->Set[Enemy]:
        enemies_set = set()
        for enemy_node in self._enemies_node.findAllMatches('**/enemy'):
            enemies_set.add(enemy_node.getPythonTag('sprite').external_object)
        return enemies_set

    def __round_ended(self)->None:
        if not self.__is_round_ended:
            self.__is_round_ended = True
            EventBus.publish('start_end_turn')