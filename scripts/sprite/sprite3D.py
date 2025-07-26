from logging import debug

from scripts.sprite.rect import Rect3D
from panda3d.core import CardMaker, TransparencyAttrib, PandaNode, CollisionNode, CollisionPolygon, Point3, Vec4, NodePath, Vec3


class Sprite3D:
    """Прямоугольный спрайт в 3d"""
    def __init__(self, rect: Rect3D, path_image:str, node:NodePath, loader, number_group:int, name_group:str):
        self._rect = rect
        self._main_node = node.attachNewNode(name_group)

        card = CardMaker(name_group)
        card.setFrame(self._rect.scale)
        self._texture_node = self._main_node.attachNewNode(card.generate())
        self._texture_node.setTag(name_group, str(number_group))

        self._texture_node.setBin(name_group, number_group)
        self._texture_node.setDepthTest(False)
        self._texture_node.setDepthWrite(False)

        texture = loader.loadTexture(path_image)
        self._texture_node.setTexture(texture)
        self._texture_node.setTransparency(TransparencyAttrib.MAlpha)

        collision = CollisionNode(name_group)
        collision.addSolid(CollisionPolygon(
            Point3(-rect.width/2, 0, -rect.height/2),
            Point3(-rect.width/2, 0, rect.height/2),
            Point3(rect.width/2, 0, rect.height/2),
            Point3(rect.width/2, 0, -rect.height/2)
        ))
        # collision.setPythonTag('collision', self)
        self._collision_node = self._main_node.attachNewNode(collision)
        self._collision_node.setPythonTag('collision', self)
        self._collision_node.show()

        self._main_node.setPos(self._rect.center[0], self._rect.center[1], 0)
        self.__rotation = Vec3(0, -90, 0)
        self._main_node.setHpr(self.__rotation)

        self.__frame = None

    def rotate(self, angle: int | float = 90):
        """Поворачивает спрайт на угол, кратный 90, вокруг заданной точки"""
        self.__rotation = Vec3(0, -90, angle)
        self._main_node.setHpr(self.__rotation)
        self._rect.rotate(angle)
        self._main_node.setPos(self._rect.center[0], self._rect.center[1], 0)

    def add_wireframe(self):
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

    def delete_wireframe(self):
        self.__frame.removeNode()

    def update(self, *args, **kwargs):
        pass

    @property
    def main_node(self)->NodePath:
        return self._main_node

    @property
    def texture_nose(self):
        return self._texture_node

    def __str__(self):
        return str(self._rect) + f' Node: {self._texture_node.getName()}'


class CopyingSprite3D(Sprite3D):
    def __init__(self, path_image:str, node:PandaNode, loader, number_group:int, name_group:str, rect:Rect3D = Rect3D(0, 0, 0, 0)):
        super().__init__(rect, path_image, node, loader, number_group, name_group)
        self.__path_image = path_image
        self.__node = node
        self.__loader = loader
        self.__layer = number_group
        self.__name_layer = name_group

    def copy(self, rect:Rect3D):
        return self.__class__(path_image=self.__path_image, node=self.__node, loader=self.__loader, layer=self.__layer, name_layer=self.__name_layer, rect=rect)

# class TestNode(Sprite3D):
#     def __init__(self, rect: Rect2D | Rect3D, path_image:str, render:Render):
#         super().__init__(rect, path_image, render)
#
#         card = CardMaker("image1")
#         card.setFrame(self._rect.scale)
#         self.child_node = super().node.attachNewNode(card.generate())
#
#         self.child_node.setPos(1, 0, 1)
#
#         self.child_node.setHpr(0, 0, 0)
#
#         texture = render.loader.loadTexture(path_image)
#         self.child_node.setTexture(texture)
#         self.child_node.setTransparency(TransparencyAttrib.MAlpha)
