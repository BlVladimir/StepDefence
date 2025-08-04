from typing import Callable

from scripts.sprite.sprite3D import Sprite3D


class UsingElementController:
    def __init__(self, using_action:Callable=lambda:None, unused_action:Callable=lambda:None):
        self._selected_sprite = None
        self._using_sprite = None
        self.__using_action = using_action
        self.__unused_action = unused_action

    def select_sprite(self, tile_sprite: Sprite3D) -> None:
        """Выделяет тайл"""
        if self._selected_sprite != tile_sprite:
            if self._selected_sprite is not None and (self._selected_sprite != self._using_sprite):
                self._selected_sprite.is_using = False
            self._selected_sprite = tile_sprite
            self._selected_sprite.is_using = True

    def unselect_sprite(self)->None:
        """Убирает выделение"""
        if self._selected_sprite and self._selected_sprite != self._using_sprite:
            self._selected_sprite.is_using = False
        self._selected_sprite = None

    def using_sprite(self)->None:
        """Назначает тайл активным"""
        if not self._using_sprite is None:
            self._using_sprite.is_using = False
            self.__unused_action()
            self._using_sprite = None
        if not self._selected_sprite is None:
            self._using_sprite = self._selected_sprite
            self._using_sprite.is_using = True
            self.__using_action()

    def unused_sprite(self)->None:
        self._using_sprite.is_using = False
        self._using_sprite = None

    @property
    def sel_using_sprite(self):
        return self._using_sprite
