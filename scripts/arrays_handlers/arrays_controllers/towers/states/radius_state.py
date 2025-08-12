from abc import ABC, abstractmethod
from logging import debug
from math import hypot

from panda3d.core import Vec2, PNMImage, Texture

from scripts.sprite.sprite3D import Sprite3D


class AbstractRadiusState(ABC):
    """Состояние, влияющее на форму радиуса башни"""

    def __init__(self, radius:float, texture:Texture):
        self.__radius = 0.5 + radius*1.2
        self._texture = texture

    @abstractmethod
    def is_in_radius(self, coordinate_center) -> bool:
        pass

    def multiply_radius(self, value:float)->None:
        self.__radius *= value

    def upgrade(self, visitor:'UpgradeVisitor')->None:
        visitor.visit_radius_state(self)

    @property
    def radius(self)->float:
        return self.__radius

    @property
    def texture(self)->Texture:
        return self._texture

    @abstractmethod
    def __str__(self)->str:
        pass

class RoundRadius(AbstractRadiusState):
    def __init__(self, radius:float, texture:Texture, coordinate_center_tower:Vec2=Vec2(0, 0)):
        super().__init__(radius, texture)
        self.__coordinate_center_tower = coordinate_center_tower

    def is_in_radius(self, sprite_enemy:Sprite3D):
        center_sprite = sprite_enemy.rect.center
        return (self.__coordinate_center_tower-center_sprite).length() <= self.radius

    def clone(self, tile):
        if tile.improved_characteristic == 'radius':
            c = tile.velue
        else:
            c = 1
        new = self.__class__(self.__radius*c, tile.rect.center)
        return new

    @property
    def texture(self)->Texture:
        return self._texture

    def __str__(self)->str:
        return str(round((self.radius-0.5)/1.2, 2))




class InfinityRadius(AbstractRadiusState):
    def __init__(self):
        super().__init__(0)

    def is_in_radius(self, coordinate_center=(0, 0)):
        return True

    def __str__(self)->str:
        return 'infinity'