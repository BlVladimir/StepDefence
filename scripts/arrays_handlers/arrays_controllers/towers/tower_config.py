from copy import copy
from math import hypot
from typing import Dict, Optional, List

import yaml
from panda3d.core import NodePath, Texture, PNMImage

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect
from scripts.arrays_handlers.arrays_controllers.enemies.damage.laser_effect import LaserEffect
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.cannon_target_state import \
    CannonTargetState
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.one_target_state import \
    OneTargetState
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.ray_state import RayState
from scripts.arrays_handlers.arrays_controllers.towers.tower_visitor import TowerVisitor
from scripts.sprite.sprites_factory import SpritesFactory


class Radius:
    


class TowerConfig:
    _instance: Optional['TowerConfig'] = None

    _textures_path: Dict[str, Dict[str, List[str]]]
    _towers_characteristics: Dict[str, Dict]

    _targets_state_dict: Dict[str, 'AbstractTargetsState']
    _visitors_dict: Dict[str, TowerVisitor]

    _charge_textures: List[Texture]
    _level_textures: List[Texture]
    _round_texture: Texture

    @classmethod
    def load_config(cls, sprite_factory: SpritesFactory, render_root:NodePath)->None:
        try:
            with open('configs/towers_config.yaml', 'r') as file:
                conf = yaml.safe_load(file)
        except Exception as Er:
            raise ValueError(Er)

        obj = cls()
        obj._textures_path = conf['textures_path']
        obj._towers_characteristics = conf['towers_characteristics']

        obj._targets_state_dict = {'one_target': OneTargetState(), 'ray': RayState(render_root),
                                     'cannon': CannonTargetState()}

        for tower in obj._towers_characteristics.keys():
            obj._towers_characteristics[tower]['radius'] = Radius(**obj._towers_characteristics[tower]['radius'])
            if 'poison' in obj._towers_characteristics[tower].keys():
                obj._towers_characteristics[tower]['poison'] = Effect(**obj._towers_characteristics[tower]['poison'])
            if 'laser' in obj._towers_characteristics[tower].keys():
                obj._towers_characteristics[tower]['laser'] = LaserEffect(**obj._towers_characteristics[tower]['laser'])

        obj._charge_textures = [sprite_factory.get_texture(texture) for texture in obj._textures_path['charge']]
        obj._level_textures = [sprite_factory.get_texture(texture) for texture in obj._textures_path['level']]

        obj._visitors_dict = {k: TowerVisitor(**obj._towers_characteristics[k]['improves']) for k in obj._towers_characteristics.keys()}

        obj._round_texture = obj.__texture_round_radius()

        cls._instance = obj

    @classmethod
    def get_charge_textures(cls):
        return cls._charge_textures

    @classmethod
    def get_level_textures(cls):
        return cls._instance._level_textures

    @classmethod
    def get_visitor_improve(cls, type_tower: str) -> TowerVisitor:
        return cls._instance._visitors_dict[type_tower]

    @classmethod
    def get_improve_cost_array(cls, type_tower: str) -> List:
        return cls._instance._towers_characteristics[type_tower]['improve_cost_array']

    @classmethod
    def get_started_characteristic_dict(cls, type_tower: str) -> Dict:
        r = {}
        for i in ['basic_damage', 'armor_piercing', 'poison', 'additional_money', 'vision', 'laser']:
            if i in cls._instance._towers_characteristics[type_tower].keys():
                r[i] = copy(cls._instance._towers_characteristics[type_tower][i])
        return r

    @classmethod
    def get_targets_state(cls, type_tower: str) -> 'OneTargetState':
        return cls._instance._targets_state_dict[cls._instance._towers_characteristics[type_tower]['targets_state']]

    @classmethod
    def get_cost(cls, type_tower: str) -> int:
        return cls._instance._towers_characteristics[type_tower]['cost']

    @classmethod
    def get_image_foundation(cls, type_tower: str) -> str:
        return cls._instance._towers_characteristics[type_tower]['foundation_image']

    @classmethod
    def get_image_gun(cls, type_tower: str) -> Optional[str]:
        return cls._instance._towers_characteristics[type_tower].get('gun_image')

    @classmethod
    def get_radius(cls, type_tower: str) -> Radius:
        return cls._instance._towers_characteristics[type_tower]['radius']

    @classmethod
    def get_round_texture(cls) -> Texture:
        return cls._instance._round_texture

    @classmethod
    def get_all_towers_name(cls):
        return list(cls._instance._towers_characteristics.keys())

    @staticmethod
    def __texture_round_radius(size: int = 512, radius_relationship: float = 0.1, brightness: int = 255) -> Texture:
        """
        Создает градиентную текстуру с плавным переходом альфа-канала.

        :param size: Размер текстуры (ширина = высота)
        :param radius_relationship: Коэффициент, определяющий ширину границы градиента
        :param brightness: Яркость цвета внутри градиента (0-255)
        :return: Объект TextTexture (Panda3D)
        """
        # Создаем PNMImage для работы с пикселями
        img = PNMImage(size, size, 4)
        radius = size / 2

        for y in range(size):
            for x in range(size):
                dx = x - radius
                dy = y - radius
                distance = hypot(dx, dy)

                # Вычисляем альфа от 0 до 1
                alpha = max((distance - (1 - radius_relationship) * radius) / (radius * radius_relationship), 0)

                if distance < radius:
                    # Применяем яркость к RGB и альфа
                    img.set_xel_a(
                        x, y,
                        brightness / 255.0,  # Красный
                        brightness / 255.0,  # Зеленый
                        brightness / 255.0,  # Синий
                        alpha  # Альфа
                    )
                else:
                    # Вне радиуса - прозрачный
                    img.set_xel_a(x, y, 0, 0, 0, 0)

        # Создаем объект текстуры из изображения
        final_texture = Texture()
        final_texture.load(img)
        return final_texture

