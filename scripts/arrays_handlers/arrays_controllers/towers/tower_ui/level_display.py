from logging import error
from typing import Tuple

from panda3d.core import NodePath, Texture, CardMaker, TransparencyAttrib


class LevelDisplay:
    def __init__(self, tower_node:NodePath, level_textures:Tuple[Texture, Texture, Texture], number:int):
        self.__level_textures = level_textures

        card = CardMaker('level_card')
        card.setFrame(-0.2, 0.2, -0.2, 0.2)
        self._charge_node = tower_node.attachNewNode(card.generate())
        self._charge_node.setPos(-0.3, 0, 0.3)

        self._charge_node.setBin('ui_tower', number)
        self._charge_node.setDepthTest(False)
        self._charge_node.setDepthWrite(False)

        self._charge_node.setTexture(self.__level_textures[0])
        self._charge_node.setTransparency(TransparencyAttrib.MAlpha)

    def set_texture(self, level:int)->None:
        try:
            self._charge_node.setTexture(self.__level_textures[level])
        except IndexError:
            error(f'Level texture {level} not found')