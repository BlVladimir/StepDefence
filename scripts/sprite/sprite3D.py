from __future__ import annotations

import copy
from typing import List

from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence

from scripts.sprite.rect import Rect3D
from panda3d.core import CardMaker, TransparencyAttrib, PandaNode, CollisionNode, CollisionPolygon, Point3, Vec4, \
    NodePath, Vec3, Vec2


class Sprite3D:
    """Прямоугольный спрайт в 3d"""
    def __init__(self, rect: Rect3D, path_image:str, parent:NodePath|Sprite3D, loader, name_group:str, number:int, external_object=None, debug_mode:bool=True):
        self._external_object = external_object

        self._rect = rect

        def create_child_nodes(node:NodePath):
            card = CardMaker(f'{name_group}_card')
            card.setFrame(self._rect.scale)
            self._texture_node = node.attachNewNode(card.generate())

            self._texture_node.setBin(name_group, number)
            self._texture_node.setDepthTest(False)
            self._texture_node.setDepthWrite(False)

            texture = loader.loadTexture(path_image)
            self._texture_node.setTexture(texture)
            self._texture_node.setTransparency(TransparencyAttrib.MAlpha)

            collision = CollisionNode(f'{name_group}_collision')
            collision.addSolid(CollisionPolygon(
                Point3(-rect.width / 2, 0, -rect.height / 2),
                Point3(-rect.width / 2, 0, rect.height / 2),
                Point3(rect.width / 2, 0, rect.height / 2),
                Point3(rect.width / 2, 0, -rect.height / 2)
            ))

            self._collision_node = node.attachNewNode(collision)
            self._collision_node.setName('sprite_collision')
            self._collision_node.setPythonTag('collision', self)
            if debug_mode:
                self._collision_node.show()

        self.__rotation_vec = Vec3(0, 0, 0)
        self.__convert_vec = Vec3(0, 0, 0)

        if isinstance(parent, NodePath):
            self._main_node = parent.attachNewNode(name_group)
            create_child_nodes(self._main_node)
            self._main_node.setPos(self._rect.center.x, self._rect.center.y, 0)
            self.__rotation_vec += Vec3(0, -90, 0)
            self._main_node.setHpr(self.__rotation_vec)
        elif isinstance(parent, Sprite3D):
            self._main_node = parent._main_node.attachNewNode(name_group)
            create_child_nodes(self._main_node)
            self.__convert_vec = Vec3(parent._rect.center.x, parent._rect.center.y, 0)

        self._main_node.setPythonTag('sprite', self)
        self.__select_frame = self.__wireframe(Vec4(0.5, 0, 0, 0.8))
        self.__select_frame.hide()
        self.__use_frame = self.__wireframe()
        self.__use_frame.hide()
        self.__is_using = False
        self.__is_selected = False
        self._debug_mode = debug_mode

    def rotate(self, angle: int | float = 90):
        """Поворачивает спрайт на угол, кратный 90, вокруг заданной точки"""
        self._main_node.setHpr(self.__rotation_vec + Vec3(0, 0, -angle))
        self._rect.rotate(angle)
        self._main_node.setPos(Vec3(self._rect.center.x, self._rect.center.y, 0)-self.__convert_vec)

    def __wireframe(self, color:Vec4 = Vec4(1, 0, 0, 1))->NodePath:
        """Добавляет проволочную обводку вокруг объекта"""
        wireframe = self._texture_node.copyTo(self._main_node)

        wireframe.clearTexture()
        wireframe.setRenderModeWireframe()
        wireframe.setColor(color)
        wireframe.setLightOff()

        wireframe.setBin("fixed", 50)
        wireframe.setDepthTest(False)
        wireframe.setDepthWrite(False)

        return wireframe

    def move(self, movement_array:List[Vec3]):
        intervals = []
        for i in range(1, len(movement_array)):
            intervals.append(
                LerpPosInterval(
                    self._main_node,
                    duration=0.1,
                    pos=movement_array[i],
                    startPos=movement_array[i - 1]
                )
            )
        sequence = Sequence(*intervals)
        sequence.start()
        vec_move = movement_array[-1] - movement_array[0]
        self._rect.move(Vec2(vec_move.x, vec_move.y))

    @property
    def main_node(self)->NodePath:
        return self._main_node

    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, value:bool):
        self.__is_selected = value and not self.__is_using
        if value:
            self.__select_frame.show()
        else:
            self.__select_frame.hide()

    @property
    def is_using(self):
        return self.__is_using

    @is_using.setter
    def is_using(self, value:bool):
        self.__is_using = value
        self.is_selected = False
        if value:
            self.__use_frame.show()
        else:
            self.__use_frame.hide()

    @property
    def rect(self):
        return copy.copy(self._rect)

    @property
    def external_object(self):
        return self._external_object

    @external_object.setter
    def external_object(self, value):
        self._external_object = value

    @property
    def debug_mode(self)->bool:
        return self._debug_mode

    def __str__(self):
        return str(self._rect) + f' Node: {self._main_node.getName()}'


class CopyingSprite3D(Sprite3D):
    def __init__(self, path_image:str, parent:PandaNode, loader, name_group:str, rect:Rect3D = Rect3D(Vec2(0, 0), 0, 0)):
        super().__init__(rect, path_image, parent, loader, name_group, 0)
        self.__path_image = path_image
        self.__loader = loader
        self.__name_layer = name_group

    def copy(self, rect:Rect3D, parent:NodePath|Sprite3D, number:int):
        return Sprite3D(path_image=self.__path_image, parent=parent, loader=self.__loader, number=number, name_group=self.__name_layer, rect=rect)
