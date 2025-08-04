from logging import debug
from typing import Optional

from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.sprite.sprite3D import Sprite3D


class Tile:
    """Класс одного тайла"""
    def __init__(self, sprite:Sprite3D, effect:str):
        self._sprite = sprite
        self._effect = effect

        self._sprite.external_object = self

    @property
    def effect(self)->str:
        return self._effect

    @property
    def sprite(self)->Sprite3D:
        return self._sprite

    @property
    def tower(self)->Optional[Tower]:
        sprite_tower = self.sprite.main_node.find('tower').getPythonTag('sprite')
        if sprite_tower:
            return sprite_tower.external_object
        return None

    def __del__(self):
        debug(f'Node {self._sprite.main_node} deleted')


