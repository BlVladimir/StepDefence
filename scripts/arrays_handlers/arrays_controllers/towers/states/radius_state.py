from abc import ABC, abstractmethod
from logging import debug
from typing import Optional

from panda3d.core import Vec2, Texture, Point3D, Point3

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.sprite.sprite3D import Sprite3D


class AbstractRadiusState(ABC):
    """Состояние, влияющее на форму радиуса башни"""

    def __init__(self, radius:float=0, texture:Texture=None):
        self.__radius = 0.5 + radius * 1.2
        self._texture = texture
        self._INVISIBLE_COEFICENT = 0.3

    @abstractmethod
    def is_in_radius(self, sprite_enemy:Sprite3D, is_not_invisible:bool=True, mouse_pos:Vec2=Vec2(0, 0)) -> bool:
        pass

    @abstractmethod
    def can_attack_target(self, enemy:Enemy, mouse_pos:Vec2=Vec2(0, 0))->bool:
        pass

    def multiply_radius(self, value:float)->None:
        self.__radius *= value

    def upgrade(self, visitor:'UpgradeVisitor')->None:
        visitor.visit_radius_state(self)

    @property
    def radius(self)->float:
        return self.__radius

    @property
    def texture(self)->Optional[Texture]:
        return self._texture

    @abstractmethod
    def __str__(self)->str:
        pass

class RoundRadius(AbstractRadiusState):
    def __init__(self, radius:float, texture:Texture, coordinate_center_tower:Vec2=Vec2(0, 0)):
        super().__init__(radius, texture)
        self.__coordinate_center_tower = coordinate_center_tower

    def is_in_radius(self, sprite_enemy:Sprite3D, is_not_invisible:bool=True, mouse_pos:Vec2=Vec2(0, 0)):
        center_sprite = sprite_enemy.rect.center
        if is_not_invisible:
            return (self.__coordinate_center_tower-center_sprite).length() <= self.radius
        return (self.__coordinate_center_tower-center_sprite).length() <= self.radius*self._INVISIBLE_COEFICENT

    def can_attack_target(self, enemy:Enemy, mouse_pos:Vec2=Vec2(0, 0))->bool:
        """Проверяет, в радиусе ли враг"""
        if 'invisible' not in enemy.characteristic:
            return self.is_in_radius(enemy.sprite)
        else:
            return self.is_in_radius(enemy.sprite, is_not_invisible=False) or (self.is_in_radius(enemy.sprite) and not enemy.sprite.external_object.characteristic['invisible'])

    def __str__(self)->str:
        return str(round((self.radius-0.5)/1.2, 2))


class InfinityRadius(AbstractRadiusState):
    def __init__(self):
        super().__init__()

    def is_in_radius(self, sprite_enemy:Sprite3D, is_not_invisible:bool=True, mouse_pos:Vec2=Vec2(0, 0)):
        return True

    def can_attack_target(self, enemy:Enemy, mouse_pos:Vec2=Vec2(0, 0))->bool:
        return True

    def __str__(self)->str:
        return 'infinity'

class InfinitySplashRadius(AbstractRadiusState):
    def __init__(self, radius:float, texture:Texture):
        super().__init__(radius-0.5, texture)

    def is_in_radius(self, sprite_enemy:Sprite3D, is_not_invisible:bool=True, mouse_pos:Vec2=Vec2(0, 0)):
        return (mouse_pos-sprite_enemy.rect.center).length() <= self.radius

    def can_attack_target(self, enemy:Enemy, mouse_pos:Vec2=Vec2(0, 0))->bool:
        return self.is_in_radius(enemy.sprite, mouse_pos=mouse_pos)

    def __str__(self)->str:
        return f'cannon {round(self.radius/1.2, 2)}'