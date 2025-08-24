from __future__ import annotations

import asyncio
from typing import Iterator

from panda3d.core import NodePath

from scripts.arrays_handlers.objects_manager import ObjectsManager
from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.enemies.group_enemies_builder import GroupEnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.arrays_handlers.selector.enemy_selector.enemy_selector import EnemySelector
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D
from scripts.sprite.sprites_factory import SpritesFactory


class EnemiesController:
    """Обработчик врагов"""
    def __init__(self, scene_gameplay_node:NodePath, sprites_factory:SpritesFactory, track:Track, mediator_controllers: 'MediatorControllers'):
        self._enemies_node = scene_gameplay_node.attachNewNode('enemy')
        self.__enemies_manager = ObjectsManager()
        self.__group_enemies_builder = GroupEnemiesBuilder(self._enemies_node, sprites_factory, track, self.__enemies_manager)

        self.__enemies_selector = EnemySelector(lambda :self.get_enemies_set())
        self.__mediator_controller = mediator_controllers
        self.__is_round_ended = False

        EventBus.subscribe('enter_click', lambda event_type, data: self.__round_ended())
        EventBus.subscribe('start_end_turn', lambda event_type, data: EventBus.publish('add_async_task', self.__move_enemies()))
        EventBus.subscribe('update_enemy', lambda event_type, data: self.__update_enemy())

    def clear_enemies(self)->None:
        """Удаоляет врагов"""
        self.__group_enemies_builder.clear_enemies()
        for enemy in self.__enemies_manager:
            enemy.sprite.external_object = None

    def create_enemies(self, wave:int, level:int, tile:Rect3D)->None:
        """Создает врагов"""
        self.__group_enemies_builder.create_enemies(wave, level, tile)

    async def __move_enemies(self)->None:
        if len(self.__enemies_manager) > 0:
            for enemy in self._enemies_node.getChildren():
                enemy.getPythonTag('sprite').external_object.end_turn()
            await asyncio.sleep(1)
            self.__update_enemy()
        EventBus.publish('complete_end_turn')
        self.__is_round_ended = False

    def __update_enemy(self):
        for enemy in self.get_enemies_set():
            enemy.update(self.__mediator_controller)


    def handle_enemy_action(self, action: str, enemy_sprite:Sprite3D = None) -> None:
        """Обрабатывает действия с врагами"""
        match action:
            case 'select':
                self.__enemies_selector.select_sprite(enemy_sprite)
            case 'unselect':
                self.__enemies_selector.unselect_sprite()
            case 'using':
                self.__enemies_selector.set_used_sprite()

    def get_enemies_set(self) -> Iterator[Enemy]:
        return iter(self.__enemies_manager)

    def __round_ended(self)->None:
        if not self.__is_round_ended:
            self.__is_round_ended = True
            EventBus.publish('start_end_turn')


if __name__ == '__main__':
    class Cl:
        a:int = 1
        b:int = 2
        c:int = 3

        def __init__(self):
            self.a = 3

    cl = Cl()
    cl1 = Cl
    cl.b = 3
    print(cl.a, cl.b, cl.c)
    print(cl1.a, cl1.b, cl1.c)