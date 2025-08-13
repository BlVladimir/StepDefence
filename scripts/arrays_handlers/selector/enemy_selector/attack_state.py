from typing import Set, Optional

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.selector.abstract_state_selector import AbstractStateSelector
from scripts.sprite.sprite3D import Sprite3D


class AttackState(AbstractStateSelector):
    def __init__(self):
        super().__init__()
        self.__tower = None
        self.__set_targets_for_attack = set()

    def get_used_sprite(self)->Optional[Sprite3D]:
        """Когда нужно получить объект для использования"""
        return self.__tower.targets_state.hit(self.__tower, main_sprite=self._main_selected_sprite, targets_set=self.__set_targets_for_attack)

    def select_sprite(self, sprite:Sprite3D)->None:
        """Логика выделения спрайта"""
        self.unselect_sprite()
        self._main_selected_sprite = sprite
        self._main_selected_sprite.is_selected = True

    def determine_set(self, enemies_set:Set[Enemy])->None:
        self.__set_targets_for_attack = self.__tower.targets_state.determine_set(enemies_set, self.__tower)

    def not_used_state(self):
        self.__clear_set()
        self.unselect_sprite()
        self.__tower = None

    def use_state(self, **kwargs):
        self.__tower = kwargs['tower']

    def unselect_sprite(self)->None:
        if self._main_selected_sprite:
            self._main_selected_sprite.is_selected = False
            if self._main_selected_sprite in self.__set_targets_for_attack:
                self._main_selected_sprite.is_special_selected = True
        self._main_selected_sprite = None

    def __clear_set(self):
        for sprite in self.__set_targets_for_attack:
            sprite.is_special_selected = False
        self.__set_targets_for_attack.clear()

    def update_set(self, enemies_set:Set[Enemy]):
        self.__clear_set()
        self.determine_set(enemies_set)