from typing import Tuple

from panda3d.core import Vec3

from scripts.sprite.convert_coordinate import ConvertCoordinate


class Rect:
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

class TestRect:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def move(self, vector: Vec3):
        """Двигает прямоугольник на заданный вектор"""
        self._x += vector.x
        self._y += vector.y

    def is_point_in(self, point: Tuple[float, float]):
        """Проверяет, находится ли точка внутри прямоугольника"""
        top_left = (self._x, self._y)
        bottom_right = (self._x + self._width, self._y + self._height)
        if top_left[0] <= point[0] <= bottom_right[0] and bottom_right[1] <= point[1] <= top_left[1]:
            return True
        else:
            return False

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