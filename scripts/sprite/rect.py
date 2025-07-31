from logging import warning
from unittest import TestCase

from panda3d.core import Vec2, Mat3

class Rect3D:
    """Класс для хранения и преобразования координат"""
    def __init__(self, top_left:Vec2, width, height, rotation_center:Vec2 = Vec2(0, 0)):
        self._top_left = top_left
        self._top_right = top_left + Vec2(width, 0)
        self._bottom_right = top_left + Vec2(width, height)
        self._bottom_left = top_left + Vec2(0, height)

        self._width = width
        self._height = height
        self.__rotation_center = rotation_center

    def move(self, vector:Vec2)->None:
        """Двигает прямоугольник на заданный вектор"""
        self._top_left += vector
        self._top_right += vector
        self._bottom_right += vector
        self._bottom_left += vector

    def rotate(self, angle: int | float = 90, name_point:str = 'rotation_center')->None:
        """Поворачивает прямоугольник на угол вокруг заданной точки"""
        match name_point:
            case 'rotation_center':
                point = self.__rotation_center
            case _:
                warning('Naim point is not dedicate')
                point = self.__rotation_center

        r_mat = Mat3.rotateMat(angle)

        self._top_left, self._bottom_right = point + r_mat.xform_vec(self._bottom_left-point), point + r_mat.xform_vec(self._top_right-point)
        self._top_right, self._bottom_left = point + r_mat.xform_vec(self._top_right-point), point + r_mat.xform_vec(self._bottom_left-point)

        self._width = max(abs(self._top_right.x-self._bottom_left.x), abs(self._top_left.x-self._bottom_right.x))
        self._height = max(abs(self._top_right.y-self._bottom_left.y), abs(self._top_left.y-self._bottom_right.y))



    @property
    def center(self)->Vec2:
        """Центр прямоугольника"""
        center = Vec2(self._top_left.x + self._width / 2, self._top_left.y + self._height / 2)
        return center

    @property
    def scale(self):
        """Для корректной отрисовки спрайта"""
        return -self._width/2, self._width/2, -self._height/2, self._height/2

    @property
    def x(self)->float:
        return self._top_left.x

    @property
    def y(self)->float:
        return self._top_left.y

    @property
    def width(self)->float:
        return self._width

    @property
    def height(self)->float:
        return self._height

    def __str__(self):
        return f'Текущий прямоугольник: ширина-{round(self._width, 2)}, высота-{round(self._height, 2)},  X-{round(self._top_left.x, 2)}, Y-{round(self._top_left.y, 2)}, центр-({round(self.center[0], 2)}, {round(self.center[1], 2)})'

class TestRect3D(TestCase):
    def setUp(self):
        self.rect = Rect3D(2, 3, 1, 2, (2.5, 3.5))
        self.rect.rotate(90)
        self.matrix = self.rect.RotationMatrix(90)

    def test_matrix(self):
        self.assertEqual(self.matrix.rotate_point((0, 0.5)), (-0.5, 0))

    def test_rotate(self):
        self.assertEqual(self.rect.__str__(), 'Текущий прямоугольник: ширина-2.0, высота-1.0,  X-1.0, Y-3.0, центр-(2.0, 3.5)')