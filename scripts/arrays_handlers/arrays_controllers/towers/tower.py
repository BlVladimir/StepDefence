from logging import debug
from typing import Optional, Dict

from panda3d.core import Point3, CardMaker, TransparencyAttrib

from scripts.arrays_handlers.arrays_controllers.towers.tower_visitor import TowerVisitor
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprite3D import Sprite3D


class Tower:
    """Класс башни"""
    def __init__(self, type_tower: str, sprite:Sprite3D, damage_dict:Dict, gun_state:Optional['GunState'], radius_state:'AbstractRadiusState', visitor_improve:'VisitorImprove', charge_display:'ChargeDisplay'):
        self._type_tower = type_tower

        self._damage_dict = damage_dict
        self.__gun_strategy = gun_state
        self.__radius_state = radius_state

        self._tower_sprite = sprite
        self._tower_sprite.external_object = self

        self.__visitor_improve = visitor_improve

        self.__is_used = False  # башня выстрелила или нет
        self.__level = 0  # уровень башни

        self._radius_node = sprite.main_node.attachNewNode('radius')
        self.__redraw_radius()

        self._is_charge = True
        self.__charge_display = charge_display

        self.__lambda_complete = lambda event_type, data:self.__set_is_charge(True)
        self.__lambda_start = lambda event_type, data:self.__set_is_charge(False)

        EventBus.subscribe('complete_end_turn', self.__lambda_complete)
        EventBus.subscribe('start_end_turn', self.__lambda_start)

    def __set_is_charge(self, value:bool)->None:
        """Меняет значе"""
        self._is_charge = value
        self.__charge_display.set_texture(value)

    def is_enemy_in_radius(self, enemy_sprite:Sprite3D)->bool:
        """Проверяет, в радиусе ли враг"""
        return self.__radius_state.is_in_radius(enemy_sprite)

    def upgrade(self)->None:
        """Улучшает башню"""
        self.__level += 1
        self.visit(self.__visitor_improve)
        debug(self._damage_dict)

    def rotate(self, mouse_point:Point3)->None:
        """Поворачивает башню"""
        if self._is_charge and self.__gun_strategy:
            self.__gun_strategy.rotate_gun(mouse_point)

    def show_radius(self)->None:
        """Визуализирует радиус"""
        debug('show radius')
        self._radius_node.show()

    def hide_radius(self)->None:
        """Скрывает радиус"""
        self._radius_node.hide()

    def unsubscribe(self):
        """До удаления"""
        EventBus.unsubscribe('complete_end_turn',self.__lambda_complete)
        EventBus.unsubscribe('start_end_turn', self.__lambda_start)

    def __redraw_radius(self):
        """Пересоздает модель радиуса"""
        card = CardMaker('radius')
        rect = self._tower_sprite.rect
        rect.width = self.__radius_state.radius * 2
        rect.height = self.__radius_state.radius * 2

        card.setFrame(rect.scale)
        self._radius_node.removeNode()
        self._radius_node = self._tower_sprite.main_node.attachNewNode(card.generate())

        self._radius_node.setBin('radius', 0)
        self._radius_node.setDepthTest(False)
        self._radius_node.setDepthWrite(False)

        self._radius_node.setTexture(self.__radius_state.gradient_texture())
        self._radius_node.setTransparency(TransparencyAttrib.MAlpha)
        self._radius_node.show()

    def visit(self, visitor:TowerVisitor):
        """Применяет visitor к характеристикам башни"""
        self.__radius_state.upgrade(visitor)
        visitor.visit_damage_dict(self._damage_dict)
        self.__redraw_radius()

    @property
    def damage_dict(self)->Dict:
        self._is_charge = False
        self.__set_is_charge(False)
        return self._damage_dict

    @property
    def is_charge(self)->bool:
        return self._is_charge

    @property
    def type_tower(self)->str:
        return self._type_tower

    @property
    def level(self)->int:
        return self.__level

    @property
    def characteristic(self)->Dict:
        characteristic = self._damage_dict.copy()
        characteristic['radius'] = str(self.__radius_state)
        return characteristic