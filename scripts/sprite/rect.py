from math import atan2, degrees, radians, sin, cos, sqrt
from typing import Tuple, List
from unittest import TestCase

from panda3d.core import Vec3

from scripts.sprite.convert_coordinate import ConvertCoordinate


class Rect2D:
    """Задает прямоугольник с заданной координатой левого верхнего угла, шириной и высотой"""

    def __init__(self, x, y, width, height, convert:ConvertCoordinate):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.__convert = convert

    def move(self, vector: Vec3):
        """Двигает прямоугольник на заданный вектор"""
        self._x += vector.x
        self._y += vector.y

    def is_point_in(self, point:Tuple[float, float]):
        """Проверяет, находится ли точка внутри прямоугольника"""
        top_left = self.__convert.convert_point((self._x, self._y))
        bottom_right = self.__convert.convert_point((self._x+self._width, self._y+self._height))
        if top_left[0] <= point[0] <= bottom_right[0] and bottom_right[1] <= point[1] <= top_left[1]:
            return True
        else:
            return False

    @property
    def center(self):
        """Центр прямоугольника"""
        center = self.__convert.convert_point((self._x + self._width / 2, self._y + self._height / 2))
        return center

    @property
    def scale(self):
        """Для корректной отрисовки спрайта"""
        return -self._width, self._width, -self.__convert.convert_y_size(self._height), self.__convert.convert_y_size(self._height)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

class Rect3D:
    class RotationMatrix:
        def __init__(self, angle: int | float):
            rad_angle = radians(angle)
            self.__matrix = ((cos(rad_angle), -sin(rad_angle)), (sin(rad_angle), cos(rad_angle)))

        def rotate_point(self, point:Tuple[int | float, int | float]):
            return [point[0]*self.__matrix[0][0] + point[1]*self.__matrix[0][1], point[0]*self.__matrix[1][0] + point[1]*self.__matrix[1][1]]

    def __init__(self, x, y, width, height, rotation_center:Tuple = (0, 0)):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.__rotation_center = rotation_center
        self.__started_scale = (self._width, self._height)

    def move(self, vector: Vec3):
        """Двигает прямоугольник на заданный вектор"""
        self._x += vector.x
        self._y += vector.y

    def is_point_in(self, point:Tuple[float, float]):
        """Проверяет, находится ли точка внутри прямоугольника"""
        top_left = (self._x, self._y)
        bottom_right = (self._x + self._width, self._y + self._height)
        if top_left[0] <= point[0] <= bottom_right[0] and bottom_right[1] <= point[1] <= top_left[1]:
            return True
        else:
            return False

    def rotate(self, angle: int | float = 90, name_point:str = 'rotation_center'):
        """Поворачивает прямоугольник на угол вокруг заданной точки"""
        match name_point:
            case 'rotation_center':
                point = self.__rotation_center
            case _:
                print('Naim point is not dedicate')
                point = self.__rotation_center

        rotation_matrix = self.RotationMatrix(angle)
        x = self._x - point[0]
        y = self._y - point[1]
        center = rotation_matrix.rotate_point((self.center[0] - point[0], self.center[1] - point[1]))

        a, c = rotation_matrix.rotate_point((x, y)), rotation_matrix.rotate_point((x+self.__started_scale[0], y+self.__started_scale[1])),
        b, d = rotation_matrix.rotate_point((x+self.__started_scale[0], y)), rotation_matrix.rotate_point((x, y+self.__started_scale[1])),

        self._width = max(abs(a[0]-c[0]), abs(b[0]-d[0]))
        self._height = max(abs(a[1] - c[1]), abs(b[1] - d[1]))

        self._x = center[0]+point[0]-self._width/2
        self._y = center[1]+point[1]-self._height/2



    @property
    def center(self):
        """Центр прямоугольника"""
        center = (self._x + self._width / 2, self._y + self._height / 2)
        return center

    @property
    def scale(self):
        """Для корректной отрисовки спрайта"""
        return -self._width/2, self._width/2, -self._height/2, self._height/2

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __str__(self):
        return f'Текущий прямоугольник: ширина-{self._width}, высота-{self._height},  X-{self._x}, Y-{self._y}, центр-{self.center}'

class TestRect3D(TestCase):
    def setUp(self):
        self.rect = Rect3D(2, 3, 1, 2, (2.5, 3.5))
        self.rect.rotate(90)
        self.matrix = self.rect.RotationMatrix(90)

    def test_matrix(self):
        self.assertEqual(self.matrix.rotate_point((0, 0.5)), (-0.5, 0))

    def test_rotate(self):
        self.assertEqual(self.rect.__str__(), 'Текущий прямоугольник: ширина-2.0, высота-1.0,  X-1.0, Y-3.0, центр-(2.0, 3.5)')