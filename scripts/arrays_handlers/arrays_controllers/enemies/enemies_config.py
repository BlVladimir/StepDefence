from logging import error
from typing import Dict, Optional

import yaml

from scripts.main_classes import rp


class EnemiesConfig:
    _instance: Optional['EnemiesConfig'] = None

    _enemies_characteristics: Dict[str, Dict]

    @classmethod
    def load_config(cls) -> None:
        """Загружает конфиг врагов один раз в память."""
        try:
            with open(rp.resource_path('configs/enemies_config.yaml'), 'r', encoding='utf-8') as file:
                conf = yaml.safe_load(file)
        except Exception as Er:
            raise ValueError(Er)
        obj = cls()
        obj._enemies_characteristics = conf['enemies_characteristics']
        cls._instance = obj

    @classmethod
    def get_characteristic(cls, type_enemy: str) -> Dict:
        """Возвращает словарь характеристик врага без поля 'image'."""
        try:
            data = cls._instance._enemies_characteristics[type_enemy]
            return {k: v for k, v in data.items() if k != 'image'}
        except Exception as Er:
            error('Error in get_enemies_characteristic')
            raise ValueError(Er)

    @classmethod
    def get_path_image(cls, type_enemy: str) -> str:
        """Возвращает путь к изображению врага из конфига."""
        try:
            return rp.resource_path(cls._instance._enemies_characteristics[type_enemy]['image'])
        except Exception as Er:
            raise ValueError(Er)


if __name__ == '__main__':
    enemies = dict(enemies_characteristics={'basic': dict(image='images2d/enemy/common.png', health=3),
                'big': dict(image='images2d/enemy/armored_enemy.png', health=6),
                'regen': dict(image='images2d/enemy/regen.png', health=4, regen=2),
                'armored': dict(image='images2d/enemy/shield_enemy.png', health=3, armor=3),
                'invisible': dict(image='images2d/enemy/invisible.png', health=4, invisible=True),
                'giant': dict(image='images2d/enemy/giant.png', health=10)
                })

    yaml.dump(enemies, open('../../../../configs/enemies_config.yaml', 'w'), default_flow_style=False, sort_keys=False)
                
                