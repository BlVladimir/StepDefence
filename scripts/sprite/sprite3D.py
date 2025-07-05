from scripts.sprite.rect import Rect
from panda3d.core import CardMaker, TransparencyAttrib

from scripts.main_classes.DTO.render import Render


class Sprite3D:
    """Прямоугольный спрайт"""
    def __init__(self, rect:Rect, path_image:str, render:Render):
        self._rect = rect

        card = CardMaker("image")
        card.setFrame(self._rect.scale)
        self._node = render.render.attachNewNode(card.generate())
        self._node.setPos(self._rect.center[0], self._rect.center[1], 0)

        self._node.setHpr(0, -90, 0)

        texture = render.loader.loadTexture(path_image)
        self._node.setTexture(texture)
        self._node.setTransparency(TransparencyAttrib.MAlpha)

    def update(self, *args, **kwargs):
        pass

    @property
    def node(self):
        return self._node