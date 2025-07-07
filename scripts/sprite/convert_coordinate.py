import unittest

class ConvertCoordinate:
    """Класс для конвертации координат с началом в левом верхнем угле и за 1 принятой шириной в двухмерные координаты panda3d"""
    def __init__(self, render):
        # self._ratio = render
        self._ratio = render.win.get_y_size()/render.win.get_x_size()

    def update_ratio(self, render):
        """Перезадает значение отношения высоты экрана к ширине"""
        self._ratio = render.win.get_y_size() / render.win.get_x_size()

    def convert_point(self, point):
        """Конвертирует точку"""
        x = point[0]*2-1
        y = point[1]*(-2/self._ratio)+1
        return x, y

    def convert_y_size(self, y_size):
        """Конвертирует значение y"""
        return y_size/self._ratio

class TestConvertCoordinate(unittest.TestCase):
    def setUp(self):
        self.object = ConvertCoordinate(0.5)

    def test_convert_point(self):
        self.assertEqual(self.object.convert_point([0.25, 0.125]), (-0.5, 0.5))
        self.assertEqual(self.object.convert_point([0.6, 0.3]), (0.2, -0.2))