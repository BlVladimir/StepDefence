from scripts.sprite.rect import Rect3D
from panda3d.core import CardMaker, TransparencyAttrib, PandaNode, Quat


class Sprite3D:
    """Прямоугольный спрайт в 3d"""
    def __init__(self, rect: Rect3D, path_image:str, node:PandaNode, loader, layer:int, name_layer:str):
        self._rect = rect

        card = CardMaker("image")
        card.setFrame(self._rect.scale)
        self._node = node.attachNewNode(card.generate())

        self._node.setBin(name_layer, layer)
        self._node.setDepthTest(False)
        self._node.setDepthWrite(False)

        self._node.setPos(self._rect.center[0], self._rect.center[1], 0)

        self._node.setHpr(0, -90, 0)

        texture = loader.loadTexture(path_image)
        self._node.setTexture(texture)
        self._node.setTransparency(TransparencyAttrib.MAlpha)

    def rotate(self, angle: int | float = 90):
        """Поворачивает спрайт на угол, кратный 90, вокруг заданной точки"""
        self._node.setHpr(0, -90, angle)
        self._rect.rotate(angle)
        self._node.setPos(self._rect.center[0], self._rect.center[1], 0)


    def update(self, *args, **kwargs):
        pass

    @property
    def node(self):
        return self._node

class CopyingSprite3D(Sprite3D):
    def __init__(self, path_image:str, node:PandaNode, loader, layer:int, name_layer:str, rect:Rect3D = Rect3D(0, 0, 0, 0)):
        super().__init__(rect, path_image, node, loader, layer, name_layer)
        self.__path_image = path_image
        self.__node = node
        self.__loader = loader
        self.__layer = layer
        self.__name_layer = name_layer

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
