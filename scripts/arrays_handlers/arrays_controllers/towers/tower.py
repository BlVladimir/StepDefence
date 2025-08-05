from logging import debug
from typing import Optional, Dict

from panda3d.core import Point3, CardMaker, TransparencyAttrib

from scripts.arrays_handlers.arrays_controllers.towers.states.gun_state import GunState
from scripts.sprite.sprite3D import Sprite3D


class Tower:
    """Класс башни"""
    def __init__(self, type_tower: str, sprite:Sprite3D, damage_dict:Dict, gun_state:Optional['GunState'], radius_state:'AbstractRadiusState', visitor_improve:'VisitorImprove'):
        self.__type_tower = type_tower

        self._damage_dict = damage_dict
        self.__gun_strategy = gun_state
        self.__radius_strategy = radius_state

        self._tower_sprite = sprite
        self._tower_sprite.external_object = self

        self.__visitor_improve = visitor_improve

        self.__is_used = False  # башня выстрелила или нет
        self.__level = 1  # уровень башни

        card = CardMaker('radius')
        rect = self._tower_sprite.rect
        rect.width = radius_state.radius*2
        rect.height = radius_state.radius*2

        card.setFrame(rect.scale)
        self._radius_node = self._tower_sprite.main_node.attachNewNode(card.generate())

        self._radius_node.setBin('radius', 0)
        self._radius_node.setDepthTest(False)
        self._radius_node.setDepthWrite(False)

        self._radius_node.setTexture(radius_state.gradient_texture())
        self._radius_node.setTransparency(TransparencyAttrib.MAlpha)
        self._radius_node.show()

    def is_enemy_in_radius(self, enemy_sprite:Sprite3D)->bool:
        return self.__radius_strategy.is_in_radius(enemy_sprite)

    def upgrade(self)->None:
        self.__radius_strategy.upgrade(self.__visitor_improve)

    def rotate(self, mouse_point:Point3)->None:
        if self.__gun_strategy:
            self.__gun_strategy.rotate_gun(mouse_point)

    def show_radius(self)->None:
        self._radius_node.show()

    def hide_radius(self)->None:
        self._radius_node.hide()

    def __del__(self):
        debug(f'Node {self._tower_sprite.main_node} deleted')

    @property
    def characteristic(self)->Dict:
        return self._damage_dict