from logging import warning
from unittest import TestCase

from panda3d.core import Vec2, Mat3, Vec3


class Rect3D:
    """Класс для хранения и преобразования координат"""
    def __init__(self, top_left:Vec2, width, height, rotation_center:Vec2 = Vec2(0, 0)):
        self._top_left = top_left
        self._top_right = top_left + Vec2(width, 0)
        self._bottom_right = top_left + Vec2(width, -height)
        self._bottom_left = top_left + Vec2(0, -height)

        self._width = width
        self._height = height
        self.__rotation_center = rotation_center

        self.__started_rect = {'top_left':self._top_left, 'top_right':self._top_right, 'bottom_right':self._bottom_right, 'bottom_left':self._bottom_left, 'center':self.center}

    def move(self, vector:Vec2)->None:
        """Двигает прямоугольник на заданный вектор"""
        self._top_left += vector
        self._top_right += vector
        self._bottom_right += vector
        self._bottom_left += vector
        self.__started_rect = {'top_left': self._top_left, 'top_right': self._top_right,
                               'bottom_right': self._bottom_right, 'bottom_left': self._bottom_left,
                               'center': self.center}

    def rotate(self, angle: int | float = 90, name_point:str = 'rotation_center')->None:
        """Поворачивает прямоугольник на угол вокруг заданной точки"""
        match name_point:
            case 'rotation_center':
                point = self.__rotation_center
            case _:
                warning('Naim point is not dedicate')
                point = self.__rotation_center

        rt = self.__started_rect  # начальный rect

        center = rt['center']
        r_mat = Mat3.rotateMat(angle)

        self._top_left, self._bottom_right = point + r_mat.xform_vec(rt['bottom_left']-point), point + r_mat.xform_vec(rt['top_right']-point)
        self._top_right, self._bottom_left = point + r_mat.xform_vec(rt['top_right']-point), point + r_mat.xform_vec(rt['bottom_left']-point)
        center = point + r_mat.xform_vec(center-point)

        self._width = max(abs(self._top_right.x-self._bottom_left.x), abs(self._top_left.x-self._bottom_right.x))
        self._height = max(abs(self._top_right.y-self._bottom_left.y), abs(self._top_left.y-self._bottom_right.y))

        self._top_left = center + Vec2(-self._width/2, self._height/2)
        self._top_right = center + Vec2(self._width/2, self._height/2)
        self._bottom_right = center + Vec2(self._width/2, -self._height/2)
        self._bottom_left = center + Vec2(-self._width/2, -self._height/2)



    @property
    def center(self)->Vec2:
        """Центр прямоугольника"""
        center = Vec2(self._top_left.x + self._width / 2, self._top_left.y - self._height / 2)
        return center

    @property
    def scale(self):
        """Для корректной отрисовки спрайта"""
        return -self._width/2, self._width/2, -self._height/2, self._height/2

    @property
    def top_left(self)->Vec2:
        return self._top_left

    @property
    def width(self)->float:
        return self._width

    @width.setter
    def width(self, value:float):
        center = self.center
        self._top_left = center + Vec2(-value / 2, self._height/2)
        self._top_right = center + Vec2(value/2, self._height/2)
        self._bottom_right = center + Vec2(value/2, -self._height/2)
        self._bottom_left = center + Vec2(-value/2, -self._height/2)
        self._width = value
        self.__started_rect = {'top_left':self._top_left, 'top_right':self._top_right,
                               'bottom_right':self._bottom_right, 'bottom_left':self._bottom_left,
                               'center':self.center}

    @property
    def height(self)->float:
        return self._height

    @height.setter
    def height(self, value:float):
        center = self.center
        self._top_left = center + Vec2(-self._width/2, value/2)
        self._top_right = center + Vec2(self._width/2, value/2)
        self._bottom_right = center + Vec2(self._width/2, -value/2)
        self._bottom_left = center + Vec2(-self._width/2, -value/2)
        self._height = value
        self.__started_rect = {'top_left': self._top_left, 'top_right': self._top_right,
                               'bottom_right': self._bottom_right, 'bottom_left': self._bottom_left,
                               'center': self.center}

    def __str__(self):
        return f'Текущий прямоугольник: ширина-{round(self._width, 2)}, высота-{round(self._height, 2)},  X-{round(self._top_left.x, 2)}, Y-{round(self._top_left.y, 2)}, центр-({round(self.center[0], 2)}, {round(self.center[1], 2)})'

    def __repr__(self):
        return f'{round(self._width, 2)}, {round(self._height, 2)}, {self.center}'

    def __copy__(self):
        return Rect3D(self._top_left, self._width, self._height, self.__rotation_center)

    @property
    def top_left(self)->Vec2:
        return self._top_left

    @property
    def top_right(self)->Vec2:
        return self._top_right

    @property
    def bottom_right(self)->Vec2:
        return self._bottom_right

    @property
    def bottom_left(self)->Vec2:
        return self._bottom_left

class TestRect3D(TestCase):
    def setUp(self):
        self.rect1 = Rect3D(Vec2(2, 3), 1, 2, Vec2(2.5, 3.5))
        self.rect2 = Rect3D(Vec2(-2, 3), 1, 2, Vec2(-1.5, 1.5))
        self.rect1.rotate(90)
        self.rect2.rotate(270)

    def test1_rotate(self):
        self.assertEqual(self.rect1.__str__(), 'Текущий прямоугольник: ширина-2.0, высота-1.0,  X-3.0, Y-4.0, центр-(4.0, 3.5)')

    def test2_rotate(self):
        self.assertEqual(self.rect2.__str__(), 'Текущий прямоугольник: ширина-2.0, высота-1.0,  X--2.0, Y-2.0, центр-(-1.0, 1.5)')