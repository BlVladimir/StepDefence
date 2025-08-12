from abc import ABC
from logging import warning
from typing import Optional

from scripts.sprite.sprite3D import Sprite3D


class AbstractStateSelector(ABC):
    """Для создания состояний выделения"""
    def __init__(self):
        self._main_selected_sprite = None

    def get_used_sprite(self)->Optional[Sprite3D]:
        """Когда нужно получить объект для использования"""
        if self._main_selected_sprite:
            self._main_selected_sprite.is_using = True
            return self._main_selected_sprite
        return None

    def select_sprite(self, sprite:Sprite3D)->None:
        """Логика выделения спрайта"""
        self.unselect_sprite()
        self._main_selected_sprite = sprite
        self._main_selected_sprite.is_selected = True

    def unselect_sprite(self)->None:
        if self._main_selected_sprite:
            self._main_selected_sprite.is_selected = False
            self._main_selected_sprite = None

    def use_state(self, **kwargs):
        warning('Use state not implemented')

    def not_used_state(self):
        self.unselect_sprite()

    @property
    def selected_sprite(self)->Optional[Sprite3D]:
        return self._main_selected_sprite