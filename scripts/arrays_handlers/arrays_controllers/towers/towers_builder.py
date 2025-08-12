from abc import ABC, abstractmethod
from logging import debug

from panda3d.core import CullBinManager

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.towers.rower_ui.charge_display import ChargeDisplay
from scripts.arrays_handlers.arrays_controllers.towers.states.gun_state import GunState
from scripts.arrays_handlers.arrays_controllers.towers.states.radius_state import RoundRadius
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.arrays_handlers.arrays_controllers.towers.towers_config import TowersConfig
from scripts.sprite.sprites_factory import SpritesFactory


class AbstractTowerBuilder(ABC):
    """Абстракция создания башни"""
    def __init__(self, sprites_factory:SpritesFactory)->None:
        self._sprites_factory = sprites_factory
        self._counter = 0

        CullBinManager.get_global_ptr().add_bin('tower', CullBinManager.BT_fixed, 2)
        CullBinManager.get_global_ptr().add_bin('gun', CullBinManager.BT_fixed, 3)
        CullBinManager.get_global_ptr().add_bin('ui_tower', CullBinManager.BT_fixed, 4)
        CullBinManager.get_global_ptr().add_bin('radius', CullBinManager.BT_fixed, 10)

    @abstractmethod
    def create_tower(self, type_tower:str, tile:Tile)->None:
        pass

    def reset_counter(self):
        self._counter = 0


class TowerBuilder(AbstractTowerBuilder):
    """Создает башни"""
    def __init__(self, sprites_factory:SpritesFactory, config:TowersConfig)->None:
        super().__init__(sprites_factory)
        self.__config = config

    def create_tower(self, type_tower:str, tile:Tile)->Tower:

        match self.__config.get_radius(type_tower).type_radius:
            case 'round':
                radius = self.__config.get_radius(type_tower).value
                texture = self.__config.round_texture
            case _:
                raise Exception('Incorrect radius type')

        characteristic = self.__config.get_started_characteristic_dict(type_tower)
        match tile.effect:
            case 'increase_damage':
                characteristic['basic_damage'] = round(characteristic['basic_damage']*1.5)
            case 'armor_piercing':
                characteristic.setdefault('armor_piercing', True)
            case 'poison':
                characteristic.setdefault('poison', Effect(0, 2))
                characteristic['poison'] += 1
            case 'additional_money':
                characteristic.setdefault('additional_money', 0)
                characteristic['additional_money'] += 1
            case 'increase_radius':
                radius *= 1.5
        debug(characteristic)


        if self.__config.get_gun(type_tower):
            gun_state = GunState(sprite=self._sprites_factory.create_sprite(tile.sprite.rect, self.__config.get_gun(type_tower),
                                                tile.sprite, 'gun', self._counter))
        else:
            gun_state = None
        sprite = self._sprites_factory.create_sprite(tile.sprite.rect, self.__config.get_image_foundation(type_tower),
                                                       tile.sprite, 'tower', self._counter)
        tower = Tower(
            type_tower=type_tower,
            sprite=sprite,
            damage_dict=characteristic,
            radius_state=RoundRadius(radius, texture, tile.sprite.rect.center),
            gun_state=gun_state,
            visitor_improve=self.__config.get_visitor_improve(type_tower),
            charge_display=ChargeDisplay(sprite.main_node, self.__config.get_charge_textures(), self._counter),
            targets_state=self.__config.get_targets_state(type_tower)
        )

        self._counter += 1

        return tower