import yaml


class MapsConfig:
    """Содержит объекты карты для копирования и их числовые значения"""
    def __init__(self):
        self._keys = {1: 'road', 2: 'road', 3:'base', 4:'basic', 5:'increase_damage', 6:'increase_radius', 7:'armor_piercing', 8:'poison', 9:'additional_money'}
        self._maps_array = [[[0, 3, 4, 4, 4],
                            [4, 1, 1, 1, 0],
                            [5, 0, 6, 1, 6],
                            [0, 1, 1, 1, 4],
                            [4, 2, 4, 0, 4]],
                            [[3, 1, 1, 1, 4],
                             [4, 5, 4, 1, 4],
                             [1, 1, 1, 1, 0],
                             [1, 4, 0, 7, 0],
                             [2, 4, 6, 0, 0]],
                            [[0, 0, 0, 0, 0, 8, 0],
                             [0, 0, 4, 7, 1, 1, 3],
                             [0, 8, 5, 0, 1, 4, 0],
                             [2, 1, 4, 1, 1, 6, 0],
                             [4, 1, 1, 1, 4, 0, 0]],
                            [[0, 4, 2, 0, 0, 0, 0],
                             [4, 1, 1, 4, 4, 6, 0],
                             [4, 1, 4, 1, 1, 0, 0],
                             [0, 1, 0, 3, 1, 0, 4],
                             [8, 1, 7, 0, 1, 4, 0],
                             [0, 1, 1, 1, 1, 4, 0],
                             [4, 0, 0, 5, 0, 0, 0]],
                            [[0, 0, 0, 0, 4, 0, 0],
                             [4, 4, 0, 1, 1, 1, 0],
                             [0, 1, 1, 1, 0, 1, 8],
                             [4, 1, 4, 9, 0, 1, 4],
                             [5, 1, 0, 0, 0, 1, 4],
                             [0, 3, 0, 6, 7, 1, 2],
                             [0, 0, 0, 0, 0, 4, 0]],
                            [[0, 0, 4, 0, 0, 4, 4],
                             [4, 1, 1, 1, 1, 1, 4],
                             [0, 3, 4, 0, 0, 1, 0],
                             [0, 0, 6, 0, 7, 1, 4],
                             [0, 4, 0, 8, 0, 1, 5],
                             [4, 0, 1, 1, 1, 1, 4],
                             [0, 4, 2, 0, 9, 0, 0]]
                            ]

    @property
    def keys(self):
        return self._keys

    @property
    def maps_array(self):
        return self._maps_array

if __name__ == '__main__':
    map = {'maps': [[[0, 3, 4, 4, 4],
                     [4, 1, 1, 1, 0],
                     [5, 0, 6, 1, 6],
                     [0, 1, 1, 1, 4],
                     [4, 2, 4, 0, 4]],
                    [[3, 1, 1, 1, 4],
                     [4, 5, 4, 1, 4],
                     [1, 1, 1, 1, 0],
                     [1, 4, 0, 7, 0],
                     [2, 4, 6, 0, 0]],
                    [[0, 0, 0, 0, 0, 8, 0],
                     [0, 0, 4, 7, 1, 1, 3],
                     [0, 8, 5, 0, 1, 4, 0],
                     [2, 1, 4, 1, 1, 6, 0],
                     [4, 1, 1, 1, 4, 0, 0]],
                    [[0, 4, 2, 0, 0, 0, 0],
                     [4, 1, 1, 4, 4, 6, 0],
                     [4, 1, 4, 1, 1, 0, 0],
                     [0, 1, 0, 3, 1, 0, 4],
                     [8, 1, 7, 0, 1, 4, 0],
                     [0, 1, 1, 1, 1, 4, 0],
                     [4, 0, 0, 5, 0, 0, 0]],
                    [[0, 0, 0, 0, 4, 0, 0],
                     [4, 4, 0, 1, 1, 1, 0],
                     [0, 1, 1, 1, 0, 1, 8],
                     [4, 1, 4, 9, 0, 1, 4],
                     [5, 1, 0, 0, 0, 1, 4],
                     [0, 3, 0, 6, 7, 1, 2],
                     [0, 0, 0, 0, 0, 4, 0]],
                    [[0, 0, 4, 0, 0, 4, 4],
                     [4, 1, 1, 1, 1, 1, 4],
                     [0, 3, 4, 0, 0, 1, 0],
                     [0, 0, 6, 0, 7, 1, 4],
                     [0, 4, 0, 8, 0, 1, 5],
                     [4, 0, 1, 1, 1, 1, 4],
                     [0, 4, 2, 0, 9, 0, 0]]
                    ],
           'keys':{1: 'road', 2: 'road', 3:'base', 4:'basic', 5:'increase_damage', 6:'increase_radius', 7:'armor_piercing', 8:'poison', 9:'additional_money'},
           'images_path':{'road':'images2d/tile/for_enemies.png',
                        'base':'images2d/tile/common_building.png',
                        'basic':'images2d/tile/common_building.png',
                        'increase_damage':'images2d/tile/damage_up.png',
                        'increase_radius':'images2d/tile/radius_up.png',
                        'armor_piercing':'images2d/tile/piercing_armor.png',
                        'poison':'images2d/tile/poison_up.png',
                        'additional_money':'images2d/tile/money_up.png'}}

    # Кастомный представитель для списков - отображаем карты в flow-стиле
    def represent_list(dumper, data):
        # Для карт (3D массивы) используем flow style
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=False)

    yaml.add_representer(list, represent_list)

    with open('../../../../configs/maps_config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(map, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
