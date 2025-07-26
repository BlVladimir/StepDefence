from unittest import TestCase


class FinderTrack:
    """Класс для поиска пути"""
    def __init__(self):
        self.__directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 0: вверх, 1: вправо, 2: вниз, 3: влево

    def find_track(self, array):
        """Ищет кротчайший путь"""
        started_x, started_y = 0, 0
        for y in range(len(array)):
            for x in range(len(array[y])):
                if array[y][x] == 2:
                    started_x, started_y = x, y
                    break
        visited = [[False] * len(array[0]) for _ in range(len(array))]
        return self.__bot(started_x, started_y, {}, visited, array)

    def __bot(self, x, y, path, visited, array):
        # Помечаем текущую клетку как посещённую
        visited[y][x] = True
        max_path = path.copy()

        for d, (dx, dy) in enumerate(self.__directions):
            new_x, new_y = x + dx, y + dy

            # Проверяем границы и доступность клетки
            if 0 <= new_x < len(array[0]) and 0 <= new_y < len(array):
                if (array[new_y][new_x] == 1 or array[new_y][new_x] == 2 or array[new_y][new_x] == 3) and not visited[new_y][new_x]:
                    # Рекурсивно исследуем новую клетку
                    n = {(x, y):d}
                    sp_path = path | n
                    new_path = self.__bot(new_x, new_y, sp_path, visited, array)
                    if len(new_path) > len(max_path):
                        max_path = new_path

        # Снимаем пометку перед возвратом для исследования других путей
        visited[y][x] = False
        return max_path

class TestFinderTrack(TestCase):
    def setUp(self):
        self.finder = FinderTrack()

    def test_find_track(self):
        a = [[2, 1, 0, 1, 1],
             [0, 1, 0, 1, 1],
             [0, 1, 1, 1, 1],
             [0, 0, 0, 1, 1],
             [0, 0, 0, 3, 0]]
        b = [[0, 3, 4, 4, 4],
             [4, 1, 1, 1, 0],
             [5, 0, 6, 1, 6],
             [0, 1, 1, 1, 4],
             [4, 2, 4, 0, 4]]

        self.assertEqual(self.finder.find_track(a), [0, 3, 3, 0, 0, 1, 1, 0, 3, 3, 3, 2, 3])
        self.assertEqual(self.finder.find_track(b), [1, 0, 0, 1, 1, 2, 2, 1])