from typing import Tuple

from panda3d.core import NodePath, Texture, CardMaker, TransparencyAttrib


class ChargeDisplay:
    def __init__(self, tower_node:NodePath, charge_textures:Tuple[Texture, Texture], number:int):
        self.__charge_texture = charge_textures[0]
        self.__not_charge_texture = charge_textures[1]

        card = CardMaker(f'charge_card')
        card.setFrame(-0.1, 0.1, -0.1, 0.1)
        self._charge_node = tower_node.attachNewNode(card.generate())
        self._charge_node.setPos(0.4, 0, 0.4)

        self._charge_node.setBin('ui_tower', number)
        self._charge_node.setDepthTest(False)
        self._charge_node.setDepthWrite(False)

        self._charge_node.setTexture(self.__charge_texture)
        self._charge_node.setTransparency(TransparencyAttrib.MAlpha)

    def set_texture(self, is_charge:bool)->None:
        if is_charge:
            self._charge_node.setTexture(self.__charge_texture)
        else:
            self._charge_node.setTexture(self.__not_charge_texture)