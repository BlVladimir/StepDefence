from typing import Set, Optional

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.selector.abstract_state_selector import AbstractStateSelector
from scripts.sprite.sprite3D import Sprite3D


class AttackState(AbstractStateSelector):
    def __init__(self):
        super().__init__()
        self.__tower = None
        self.__set_possible_for_attack = set()

    def get_used_sprite(self)->Optional[Sprite3D]:
        """Когда нужно получить объект для использования"""
        if self._main_selected_sprite:
            if self._main_selected_sprite in self.__set_possible_for_attack and self.__tower.is_charge:
                self._main_selected_sprite.external_object.hit(self.__tower.damage_dict)
                return None
            return self._main_selected_sprite
        return None

    def select_sprite(self, sprite:Sprite3D)->None:
        """Логика выделения спрайта"""
        self.unselect_sprite()
        self._main_selected_sprite = sprite
        self._main_selected_sprite.is_selected = True

    def determine_set(self, enemies_set:Set[Enemy])->None:
        for enemy in enemies_set:
            if self.__tower.is_enemy_in_radius(enemy.sprite):
                enemy.sprite.is_special_selected = True
                self.__set_possible_for_attack.add(enemy.sprite)

    def not_used_state(self):
        self.__clear_set()
        self.unselect_sprite()
        self.__tower = None

    def use_state(self, **kwargs):
        self.__tower = kwargs['tower']

    def unselect_sprite(self)->None:
        if self._main_selected_sprite:
            self._main_selected_sprite.is_selected = False
            if self._main_selected_sprite in self.__set_possible_for_attack:
                self._main_selected_sprite.is_special_selected = True
        self._main_selected_sprite = None

    def __clear_set(self):
        for sprite in self.__set_possible_for_attack:
            sprite.is_special_selected = False
        self.__set_possible_for_attack.clear()

    def update_set(self, enemies_set:Set[Enemy]):
        self.__clear_set()
        self.determine_set(enemies_set)