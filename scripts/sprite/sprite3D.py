from __future__ import annotations

from scripts.sprite.rect import Rect3D
from panda3d.core import CardMaker, TransparencyAttrib, PandaNode, CollisionNode, CollisionPolygon, Point3, Vec4, NodePath, Vec3

class Sprite3D:
    """Прямоугольный спрайт в 3d"""
    def __init__(self, rect: Rect3D, path_image:str, parent:NodePath|Sprite3D, loader, name_group:str, number:int, external_object=None):
        self._external_object = external_object

        self._rect = rect

        def create_child_nodes(node:NodePath):
            card = CardMaker(name_group)
            card.setFrame(self._rect.scale)
            self._texture_node = node.attachNewNode(card.generate())

            self._texture_node.setBin(name_group, number)
            self._texture_node.setDepthTest(False)
            self._texture_node.setDepthWrite(False)

            texture = loader.loadTexture(path_image)
            self._texture_node.setTexture(texture)
            self._texture_node.setTransparency(TransparencyAttrib.MAlpha)

            collision = CollisionNode(name_group)
            collision.addSolid(CollisionPolygon(
                Point3(-rect.width / 2, 0, -rect.height / 2),
                Point3(-rect.width / 2, 0, rect.height / 2),
                Point3(rect.width / 2, 0, rect.height / 2),
                Point3(rect.width / 2, 0, -rect.height / 2)
            ))

            self._collision_node = node.attachNewNode(collision)
            self._collision_node.setPythonTag('collision', self)
            self._collision_node.show()

        if isinstance(parent, NodePath):
            self._main_node = parent.attachNewNode(name_group)
            create_child_nodes(self._main_node)
            self._main_node.setPos(self._rect.center[0], self._rect.center[1], 0)
            self._main_node.setHpr(Vec3(0, -90, 0))
        elif isinstance(parent, Sprite3D):
            self._main_node = parent._main_node.attachNewNode(name_group)
            create_child_nodes(self._main_node)
        else:
            raise ValueError('Incorrect type of parent')

        self.__frame = None

        self.__is_using = False

    def rotate(self, angle: int | float = 90):
        """Поворачивает спрайт на угол, кратный 90, вокруг заданной точки"""
        self._main_node.setHpr(Vec3(0, -90, angle))
        self._rect.rotate(angle)
        self._main_node.setPos(self._rect.center[0], self._rect.center[1], 0)

    def __add_wireframe(self):
        """Добавляет проволочную обводку вокруг объекта"""
        if not self.__frame:
            wireframe = self._texture_node.copyTo(self._main_node)

            wireframe.clearTexture()
            wireframe.setRenderModeWireframe()
            wireframe.setColor(1, 0, 0, 1)  # Красный цвет
            wireframe.setLightOff()

            wireframe.setBin("fixed", 50)
            wireframe.setDepthTest(False)
            wireframe.setDepthWrite(False)

            self.__frame = wireframe

    def __delete_wireframe(self):
        self.__frame.removeNode()

    def update(self, *args, **kwargs):
        pass

    @property
    def main_node(self)->NodePath:
        return self._main_node

    @property
    def texture_nose(self):
        return self._texture_node

    @property
    def is_using(self):
        return self.__is_using

    @is_using.setter
    def is_using(self, value:bool):
        self.__is_using = value
        if value:
            self.__add_wireframe()
        else:
            self.__delete_wireframe()

    @property
    def rect(self):
        return self._rect

    @property
    def external_object(self):
        return self._external_object

    @external_object.setter
    def external_object(self, value):
        self._external_object = value

    def __str__(self):
        return str(self._rect) + f' Node: {self._main_node.getName()}'


class CopyingSprite3D(Sprite3D):
    def __init__(self, path_image:str, parent:PandaNode, loader, name_group:str, rect:Rect3D = Rect3D(0, 0, 0, 0)):
        super().__init__(rect, path_image, parent, loader, name_group, 0)
        self.__path_image = path_image
        self.__loader = loader
        self.__name_layer = name_group

    def copy(self, rect:Rect3D, parent:NodePath|Sprite3D, number:int):
        return Sprite3D(path_image=self.__path_image, parent=parent, loader=self.__loader, number=number, name_group=self.__name_layer, rect=rect)
