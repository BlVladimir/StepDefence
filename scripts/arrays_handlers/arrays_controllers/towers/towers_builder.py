from abc import ABC, abstractmethod
from logging import debug

from panda3d.core import CullBinManager

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.towers.tower_config import TowerConfig
from scripts.arrays_handlers.arrays_controllers.towers.tower_ui.charge_display import ChargeDisplay
from scripts.arrays_handlers.arrays_controllers.towers.states.gun_state import GunState
from scripts.arrays_handlers.arrays_controllers.towers.states.radius_state import RoundRadius, InfinityRadius, \
    InfinitySplashRadius
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.arrays_handlers.arrays_controllers.towers.tower_ui.level_display import LevelDisplay
from scripts.arrays_handlers.arrays_controllers.towers.tower_visitor import TowerVisitor
from scripts.arrays_handlers.objects_manager import ObjectsManager
from scripts.sprite.sprites_factory import SpritesFactory


class AbstractTowerBuilder(ABC):
    """Абстракция создания башни"""
    def __init__(self, sprites_factory:SpritesFactory)->None:
        self._sprites_factory = sprites_factory

        CullBinManager.get_global_ptr().add_bin('tower', CullBinManager.BT_fixed, 2)
        CullBinManager.get_global_ptr().add_bin('gun', CullBinManager.BT_fixed, 3)
        CullBinManager.get_global_ptr().add_bin('ui_tower', CullBinManager.BT_fixed, 4)
        CullBinManager.get_global_ptr().add_bin('radius', CullBinManager.BT_fixed, 10)

    @abstractmethod
    def create_tower(self, type_tower:str, tile:Tile)->None:
        pass

class TowerBuilder(AbstractTowerBuilder):
    """Создает башни"""
    def __init__(self, sprites_factory:SpritesFactory, tower_manager:ObjectsManager)->None:
        super().__init__(sprites_factory)
        self.__tower_mng = tower_manager

    def create_tower(self, type_tower:str, tile:Tile)->Tower:

        match TowerConfig.get_radius(type_tower).type_radius:
            case 'round':
                radius = RoundRadius(TowerConfig.get_radius(type_tower).value, TowerConfig.get_round_texture(), tile.sprite.rect.center)
            case 'infinity':
                radius = InfinityRadius()
            case 'infinity_splash':
                radius = InfinitySplashRadius(TowerConfig.get_radius(type_tower).value, TowerConfig.get_round_texture())
            case _:
                raise Exception('Incorrect radius type')

        characteristic = TowerConfig.get_started_characteristic_dict(type_tower)
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
                radius.upgrade(TowerVisitor(radius=1.5))
        debug(characteristic)


        if TowerConfig.get_gun_texture(type_tower):
            gun_state = GunState(sprite=self._sprites_factory.create_sprite(tile.sprite.rect, TowerConfig.get_gun_texture(type_tower),
                                                                            tile.sprite, 'gun', len(self.__tower_mng)))
        else:
            gun_state = None
        sprite = self._sprites_factory.create_sprite(tile.sprite.rect, TowerConfig.get_foundation_texture(type_tower),
                                                       tile.sprite, 'tower', len(self.__tower_mng))
        tower = Tower(
            type_tower=type_tower,
            sprite=sprite,
            damage_dict=characteristic,
            radius_state=radius,
            gun_state=gun_state,
            visitor_improve=TowerConfig.get_visitor_improve(type_tower),
            charge_display=ChargeDisplay(sprite.main_node, TowerConfig.get_charge_textures(), len(self.__tower_mng)),
            level_display=LevelDisplay(sprite.main_node, TowerConfig.get_level_textures(), len(self.__tower_mng)),
            targets_state=TowerConfig.get_targets_state(type_tower)
        )

        self.__tower_mng + tower

        return tower