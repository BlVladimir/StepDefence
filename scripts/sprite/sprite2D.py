from scripts.sprite.rect import Rect2D
from panda3d.core import CardMaker, TransparencyAttrib, PandaNode

from scripts.main_classes.interaction.rendermanager import RenderManager


class Sprite2D:
    """Прямоугольный спрайт"""
    def __init__(self, rect:Rect2D, path_image:str, node:PandaNode, loader):
        self._rect = rect

        card = CardMaker("image")
        card.setFrame(self._rect.scale)
        self._node = node.attachNewNode(card.generate())
        self._node.setPos(self._rect.center[0], 0, self._rect.center[1])

        texture = loader.loadTexture(path_image)
        self._node.setTexture(texture)
        self._node.setTransparency(TransparencyAttrib.MAlpha)

    def update(self, *args, **kwargs):
        pass

    @property
    def node(self):
        return self._node

    @property
    def rect(self):
        return self._rect