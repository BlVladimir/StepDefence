class MapsConfig:
    """Содержит объекты карты для копирования и их числовые значения"""
    def __init__(self):
        self._keys = {1: 'road', 2: 'road', 3:'base', 4:'basic', 5:'increase_damage', 6:'increase_radius', 7:'piercing_armor', 8:'poison', 9:'additional_money'}
        self._maps_array = [[[0, 3, 4, 4, 4],
                            [4, 1, 1, 1, 0],
                            [5, 0, 6, 1, 6],
                            [0, 1, 1, 1, 4],
                            [4, 2, 4, 0, 4]],
                            [[2, 1, 0, 1, 1],
                             [0, 1, 0, 1, 1],
                             [0, 1, 1, 1, 1],
                             [0, 0, 0, 1, 1],
                             [0, 0, 0, 3, 0]]]

    @property
    def keys(self):
        return self._keys

    @property
    def maps_array(self):
        return self._maps_array

if __name__ == '__main__':
    keys = {1: 'road', 2: 'base', 3 | 9: 'basic', 4: 'increase_damage', 5: 'increase_radius', 6: 'piercing_armor', 7: 'poison', 8: 'additional_money'}
    print(keys[3 | 9])
    print(keys[9])