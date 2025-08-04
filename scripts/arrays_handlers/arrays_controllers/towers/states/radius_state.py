from abc import ABC, abstractmethod
from logging import debug
from math import hypot

from panda3d.core import Vec2, PNMImage, Texture

from scripts.sprite.sprite3D import Sprite3D


class AbstractRadiusState(ABC):
    """Состояние, влияющее на форму радиуса башни"""

    def __init__(self, radius:float):
        self.__radius = 0.5 + radius*1.2

    @abstractmethod
    def is_in_radius(self, coordinate_center) -> bool:
        pass

    def multiply_radius(self, value:float)->None:
        self.__radius *= value

    def upgrade(self, visitor:'UpgradeVisitor')->None:
        visitor.visit_radius_strategy(self)

    @property
    def radius(self)->float:
        return self.__radius

    @staticmethod
    @abstractmethod
    def gradient_texture(size:int, radius_relationship:float, brightness:int)->Texture:
        pass

class RoundRadius(AbstractRadiusState):
    def __init__(self, radius:float, coordinate_center_tower:Vec2=Vec2(0, 0)):
        super().__init__(radius)
        self.__coordinate_center_tower = coordinate_center_tower

    def is_in_radius(self, sprite_enemy:Sprite3D):
        center_sprite = sprite_enemy.rect.center
        debug(f'length:{(self.__coordinate_center_tower-center_sprite).length()} radius: {self.radius}')
        if (self.__coordinate_center_tower-center_sprite).length() <= self.radius:
            return True
        else:
            return False

    def clone(self, tile):
        if tile.improved_characteristic == 'radius':
            c = tile.velue
        else:
            c = 1
        new = self.__class__(self.__radius*c, tile.rect.center)
        return new

    @staticmethod
    def gradient_texture(size:int=512, radius_relationship:float=0.1, brightness:int=255):
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




class InfinityRadius(AbstractRadiusState):
    def __init__(self):
        super().__init__(0)

    def is_in_radius(self, coordinate_center=(0, 0)):
        return True