from copy import copy
from math import hypot
from typing import Tuple, Dict, Optional

from panda3d.core import Texture, PNMImage, NodePath

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect
from scripts.arrays_handlers.arrays_controllers.enemies.damage.laser_effect import LaserEffect
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.cannon_target_state import CannonTargetState
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.one_target_state import \
    OneTargetState
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.ray_state import RayState
from scripts.arrays_handlers.arrays_controllers.towers.tower_visitor import TowerVisitor
from scripts.sprite.sprites_factory import SpritesFactory


class Radius:
    def __init__(self, value: float = 0.0, type_radius: str = 'round'):
        self._value = value
        self._type_radius = type_radius

    @property
    def value(self):
        return self._value

    @property
    def type_radius(self):
        return self._type_radius


class TowersConfig:
    """Содержит объекты башен для копирования и их числовые значения"""

    def __init__(self, sprite_factory: SpritesFactory, render_root:NodePath):
        self._round_texture = self.__texture_round_radius()
        self.__targets_state_dict = {'one_target': OneTargetState(), 'ray': RayState(render_root),
                                     'cannon': CannonTargetState()}
        self.__products = {
            'basic': dict(basic_damage=2, cost=3, radius=Radius(1), improve_cost_array=(4, 6), additional_money=2,
                          targets_state='one_target'),
            'sniper': dict(basic_damage=4, cost=5, radius=Radius(2), improve_cost_array=(6, 8),
                           targets_state='one_target'),
            'anty_shield': dict(basic_damage=3, cost=4, radius=Radius(1.5), improve_cost_array=(5, 7),
                                armor_piercing=True, targets_state='one_target'),
            'venom': dict(basic_damage=2, cost=5, radius=Radius(1), improve_cost_array=(4, 6), poison=Effect(2, 2),
                          targets_state='one_target'),
            'anty_invisible': dict(basic_damage=3, cost=4, radius=Radius(1.5), improve_cost_array=(6, 8), vision=True,
                                   targets_state='one_target'),
            'cutter': dict(basic_damage=2, cost=5, radius=Radius(type_radius='infinity'), improve_cost_array=(8, 10),
                           targets_state='ray'),
            'laser': dict(basic_damage=0, cost=6, radius=Radius(1.5), improve_cost_array=(8, 10), laser=LaserEffect(0),
                          targets_state='one_target'),
            'cannon': dict(basic_damage=3, cost=8, radius=Radius(value=0.5, type_radius='infinity_splash'),
                           improve_cost_array=(10, 12), targets_state='cannon')
        }

        self.__sprites_towers_foundations_dict = {
            'basic': "images2d/tower/common_foundation.png",
            'sniper': "images2d/tower/sniper_foundation.png",
            'anty_shield': "images2d/tower/anty_shield.png",
            'venom': "images2d/tower/venom_foundation.png",
            'anty_invisible': "images2d/tower/anty_invisibility_tower.png",
            'cutter': 'images2d/tower/cutter_foundation.png',
            'laser': 'images2d/tower/laser_foundation.png',
            'cannon': 'images2d/tower/cannon.png'
        }

        self.__sprites_towers_guns_dict = {
            'basic': "images2d/tower/common_gun.png",
            'sniper': "images2d/tower/sniper_gun.png",
            'venom': "images2d/tower/venom_gun.png",
            'cutter': 'images2d/tower/cutter_gun.png',
            'laser': 'images2d/tower/laser_gun.png'
        }

        self.__visitors_dict = {
            'basic': TowerVisitor(basic_damage=2, radius=1.2),
            'sniper': TowerVisitor(basic_damage=2, radius=1.2),
            'anty_shield': TowerVisitor(basic_damage=2, radius=1.2),
            'venom': TowerVisitor(basic_damage=2, radius=1.2),
            'anty_invisible': TowerVisitor(basic_damage=2, radius=1.2),
            'cutter': TowerVisitor(basic_damage=1),
            'laser': TowerVisitor(radius=1.2),
            'cannon': TowerVisitor(basic_damage=1)
        }

        self.__charge_textures = (sprite_factory.get_texture('images2d/UI/enemy_characteristic/charged.png'),
                                  sprite_factory.get_texture('images2d/UI/enemy_characteristic/not_charged.png'))

    def get_charge_textures(self) -> Tuple[Texture, Texture]:
        return self.__charge_textures

    def get_visitor_improve(self, type_tower: str) -> TowerVisitor:
        return self.__visitors_dict[type_tower]

    def get_improve_cost_array(self, type_tower: str) -> Tuple:
        return self.__products[type_tower]['improve_cost_array']

    def get_started_characteristic_dict(self, type_tower: str) -> Dict:
        r = {}
        for i in ['basic_damage', 'armor_piercing', 'poison', 'additional_money', 'vision', 'laser']:
            if i in self.__products[type_tower].keys():
                r[i] = copy(self.__products[type_tower][i])
        return r

    def get_targets_state(self, type_tower: str) -> 'OneTargetState':
        return self.__targets_state_dict[self.__products[type_tower]['targets_state']]

    def get_cost(self, type_tower: str) -> int:
        return self.__products[type_tower]['cost']

    def get_image_foundation(self, type_tower: str) -> str:
        return self.__sprites_towers_foundations_dict[type_tower]

    def get_gun(self, type_tower: str) -> Optional[str]:
        if type_tower in self.__sprites_towers_guns_dict.keys():
            return self.__sprites_towers_guns_dict[type_tower]
        return None

    def get_radius(self, type_tower: str) -> Radius:
        return self.__products[type_tower]['radius']

    @property
    def round_texture(self) -> Texture:
        return self._round_texture

    @staticmethod
    def __texture_round_radius(size: int = 512, radius_relationship: float = 0.1, brightness: int = 255):
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
