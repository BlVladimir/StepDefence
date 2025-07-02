from panda3d.core import Vec3

class Rect:
    def __init__(self, x, y, width, height):
        """Задает прямоугольник с заданной координатой левого верхнего угла, шириной и высотой"""
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def move(self, vector: Vec3):
        """Двигает прямоугольник на заданный вектор"""
        self._x += vector.x
        self._y += vector.y

    @property
    def center(self):
        """Центр прямоугольника"""
        return self._x + self._width / 2, self._y + self._height / 2

    @property
    def scale(self):
        """Для корректной отрисовки спрайта"""
        return 0, -self._width, self._height, 0

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y