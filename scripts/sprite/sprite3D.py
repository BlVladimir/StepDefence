from __future__ import annotations

from copy import copy
from typing import Any

from scripts.sprite.rect import Rect3D
from panda3d.core import CardMaker, TransparencyAttrib, CollisionNode, Point3, NodePath, Vec3, BitMask32, CollisionBox, Loader


class Sprite3D:
    """Прямоугольный спрайт в 3d"""
    def __init__(self, rect: Rect3D, path_image:str, parent:NodePath|Sprite3D, loader:Loader, name_group:str, number:int, external_object=None, debug_mode:bool=True):
        self._external_object = external_object

        self._rect = rect

        self.__rotation_vec = Vec3(0, 0, 0)
        self.__convert_vec = Vec3(0, 0, 0)

        self._debug_mode = debug_mode
        if isinstance(parent, NodePath):
            self._main_node = parent.attachNewNode(name_group)
            self.__setup_node(rect, path_image, loader, name_group, number)
            self._main_node.setPos(self._rect.center.x, self._rect.center.y, 0)
            self.__rotation_vec += Vec3(0, -90, 0)
            self._main_node.setHpr(self.__rotation_vec)
        else:
            self._main_node = parent._main_node.attachNewNode(name_group)
            self.__setup_node(rect, path_image, loader, name_group, number)
            self.__convert_vec = Vec3(parent._rect.center.x, parent._rect.center.y, 0)

        self._main_node.setPythonTag('sprite', self)

    def rotate(self, angle: int | float = 90):
        """Поворачивает спрайт на угол, кратный 90, вокруг заданной точки"""
        self._main_node.setHpr(self.__rotation_vec + Vec3(0, 0, -angle))
        self._rect.rotate(angle)
        self._main_node.setPos(Vec3(self._rect.center.x, self._rect.center.y, 0)-self.__convert_vec)

    @property
    def main_node(self)->NodePath:
        return self._main_node

    @property
    def rect(self):
        return copy(self._rect)

    @property
    def external_object(self):
        return self._external_object

    @external_object.setter
    def external_object(self, value:Any):
        self._external_object = value

    @property
    def debug_mode(self)->bool:
        return self._debug_mode

    def __str__(self):
        return str(self._rect) + f' Node: {self._main_node.getName()}'

    def __setup_node(self, rect:Rect3D, path_image:str, loader:Loader, name_group:str, number:int):
        card = CardMaker(f'{name_group}_card')
        card.setFrame(self._rect.scale)
        self._texture_node = self._main_node.attachNewNode(card.generate())

        self._texture_node.setBin(name_group, number)
        self._texture_node.setDepthTest(False)
        self._texture_node.setDepthWrite(False)

        texture = loader.loadTexture(path_image)
        self._texture_node.setTexture(texture)
        self._texture_node.setTransparency(TransparencyAttrib.MAlpha)

        collision = CollisionNode(f'{name_group}_collision')
        collision.addSolid(CollisionBox(Point3(rect.width / 2, -0.01, rect.height / 2),
                                        Point3(-rect.width / 2, 0.01, -rect.height / 2)))
        collision.setIntoCollideMask(BitMask32.bit(1) | BitMask32.bit(2))

        self._collision_node = self._main_node.attachNewNode(collision)
        self._collision_node.setName('sprite_collision')
        self._collision_node.setPythonTag('collision', self)
        if self._debug_mode:
            self._collision_node.show()