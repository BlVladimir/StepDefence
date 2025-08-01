from panda3d.core import Point3, Vec2, Vec3

from scripts.sprite.sprite3D import Sprite3D


class GunState:
    """Состояние, влияющее на пушку башни"""
    def __init__(self, sprite:Sprite3D):
        self.__sprite = sprite

    def rotate_gun(self, mouse_point:Point3)->None:  # поворачивает ствол в сторону мышки
        center = self.__sprite.rect.center
        vec = Vec2(mouse_point.x, mouse_point.y) - center
        self.__sprite.rotate(
            -vec.signedAngleDeg(Vec2(1, 0))-90
        )

    @property
    def gun_sprite(self):
        return self.__sprite
