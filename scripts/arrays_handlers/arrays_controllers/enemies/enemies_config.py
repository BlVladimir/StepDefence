from logging import error
from typing import Dict, Optional, Tuple

import yaml
from panda3d.core import Texture, Loader, PNMImage

from scripts.main_classes import rp


class EnemiesConfig:
    _instance: Optional['EnemiesConfig'] = None

    _enemies_characteristics: Dict[str, Dict]
    _enemies_textures: Dict[str, Tuple[Texture, Texture]]

    @classmethod
    def load_config(cls, loader:Loader) -> None:
        """Загружает конфиг врагов один раз в память."""
        try:
            with open(rp.resource_path('configs/enemies_config.yaml'), 'r', encoding='utf-8') as file:
                conf = yaml.safe_load(file)
        except Exception as Er:
            raise ValueError(Er)
        obj = cls()
        obj._enemies_characteristics = conf['enemies_characteristics']
        obj._enemies_textures = {enm:cls.__get_textures(conf['enemies_characteristics'][enm]['image'], loader) for enm in conf['enemies_characteristics'].keys()}

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
    def get_textures(cls, type_enemy)->Tuple[Texture, Texture]:
        return cls._instance._enemies_textures[type_enemy]

    @staticmethod
    def __get_textures(path_image: str, loader:Loader) -> Tuple[Texture, Texture]:
        first_texture = loader.loadTexture(path_image)
        img = PNMImage()
        img.read(path_image)
        for x in range(img.get_x_size()):
            for y in range(img.get_y_size()):
                r, g, b, a = img.getXelA(x, y)
                if a > 0:
                    img.setXelA(x, y, r, g, b, a*0.3)
        second_texture = Texture("processed_texture")
        second_texture.load(img)
        return first_texture, second_texture


if __name__ == '__main__':
    enemies = dict(enemies_characteristics={'basic': dict(image='images2d/enemy/common.png', health=3),
                'big': dict(image='images2d/enemy/armored_enemy.png', health=6),
                'regen': dict(image='images2d/enemy/regen.png', health=4, regen=2),
                'armored': dict(image='images2d/enemy/shield_enemy.png', health=3, armor=3),
                'invisible': dict(image='images2d/enemy/invisible.png', health=4, invisible=True),
                'giant': dict(image='images2d/enemy/giant.png', health=10)
                })

    yaml.dump(enemies, open('../../../../configs/enemies_config.yaml', 'w'), default_flow_style=False, sort_keys=False)
                
                