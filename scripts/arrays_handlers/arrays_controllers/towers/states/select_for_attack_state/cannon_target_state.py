from logging import debug
from typing import Set

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.abstract_targets_state import \
    AbstractTargetsState
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.sprite.sprite3D import Sprite3D


class CannonTargetState(AbstractTargetsState):
    """"""
    @staticmethod
    def determine_set(enemies_set:Set[Enemy], tower:Tower, **kwargs)->Set[Sprite3D]:
        """Как определить множество врагов для выстрела"""
        targets_set = set()
        for enemy in enemies_set:
            if tower.can_attack_target(enemy.sprite):
                enemy.sprite.is_special_selected = True
                targets_set.add(enemy.sprite)
        # debug(f'targets_set: {len(targets_set)}')
        return targets_set

    def hit(self, tower:Tower, **kwargs)->None:
        """В каких врагов стрелять"""
        if kwargs['targets_set']:
            if self.__hit_condition(tower, **kwargs):
                for enemy in kwargs['targets_set']:
                    enemy.external_object.hit(tower.damage_dict(enemy.external_object))
        elif kwargs['main_sprite']:
            return kwargs['main_sprite']
        return None

    @staticmethod
    def __hit_condition(tower:Tower, **kwargs)->bool:
        return tower.is_charge

    def __str__(self):
        return 'cannon'