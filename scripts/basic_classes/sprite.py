from direct.showbase.ShowBase import ShowBase

from scripts.basic_classes.rect import Rect
from panda3d.core import CardMaker, TransparencyAttrib

class Sprite:
    def __init__(self, rect:Rect, path_image:str, show_base:ShowBase):
        """Прямоугольный спрайт"""
        self._rect = rect

        card = CardMaker("image")
        card.setFrame(self._rect.scale)
        self._node = show_base.render.attachNewNode(card.generate())
        self._node.setPos(self._rect.x, self._rect.y, 0)

        self._node.setHpr(0, -90, 0)

        texture = show_base.loader.loadTexture(path_image)
        self._node.setTexture(texture)
        self._node.setTransparency(TransparencyAttrib.MAlpha)

    def update(self, *args, **kwargs):
        pass

    @property
    def node(self):
        return self._node