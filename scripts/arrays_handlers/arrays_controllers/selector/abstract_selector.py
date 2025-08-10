from abc import ABC
from logging import error
from typing import Optional

from scripts.arrays_handlers.arrays_controllers.selector.abstract_state_selector import AbstractStateSelector
from scripts.sprite.sprite3D import Sprite3D


class AbstractSelector(ABC):
    def __init__(self, current_state_name, **state_dict:AbstractStateSelector):
        self._used_sprite = None
        self._state_dict = state_dict
        self._current_state_name = current_state_name

    def set_used_sprite(self)->None:
        try:
            if self._used_sprite:
                self._used_sprite.is_using = False
            self._used_sprite = self._state_dict[self._current_state_name].get_used_sprite()
            self._state_dict[self._current_state_name].unselect_sprite()
        except KeyError:
            error('State not found')

    def select_sprite(self, sprite:Sprite3D)->None:
        try:
            self._state_dict[self._current_state_name].select_sprite(sprite)
        except KeyError:
            error('State not found')

    def change_state(self, state_name:str)->None:
        try:
            self._state_dict[self._current_state_name].unselect_sprite()
            self._current_state_name = state_name
        except KeyError:
            error('State not found')

    def unselect_sprite(self)->None:
        self._state_dict[self._current_state_name].unselect_sprite()

    @property
    def used_sprite(self)->Optional[Sprite3D]:
        return self._used_sprite

