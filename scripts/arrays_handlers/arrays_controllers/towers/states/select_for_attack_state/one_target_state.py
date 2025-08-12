from typing import Set

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.abstract_targets_state import \
    AbstractTargetsState
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.sprite.sprite3D import Sprite3D


class OneTargetState(AbstractTargetsState):
    """Башня стреляет в одну цель"""
    @staticmethod
    def determine_set(enemies_set:Set[Enemy], tower:Tower, **kwargs)->Set[Sprite3D]:
        """Как определить множество врагов для выстрела"""
        targets_set = set()
        for enemy in enemies_set:
            if tower.is_enemy_in_radius(enemy.sprite):
                enemy.sprite.is_special_selected = True
                targets_set.add(enemy.sprite)
        return targets_set

    def hit(self, tower:Tower, **kwargs)->None:
        """В каких врагов стрелять"""
        if self.hit_condition(tower, **kwargs):
            kwargs['main_sprite'].external_object.hit(tower.damage_dict)

    @staticmethod
    def hit_condition(tower:Tower, **kwargs)->bool:
        return kwargs['main_sprite'] in kwargs['targets_set'] and tower.is_charge