from logging import error
from typing import Dict

import yaml
from pydantic import BaseModel


class EnemiesConfig(BaseModel):
    enemies_characteristics: Dict

    def get_characteristic(self, type_enemy:str)->Dict:
        """Возвращает словарь характеристик врага без поля 'image'."""
        try:
            data = self.enemies_characteristics[type_enemy]
            return {k: v for k, v in data.items() if k != 'image'}
        except Exception as Er:
            error('Error in get_enemies_characteristic')
            raise ValueError(Er)

    def get_path_image(self, type_enemy:str)->str:
        """Возвращает путь к изображению врага из конфига."""
        try:
            return self.enemies_characteristics[type_enemy]['image']
        except Exception as Er:
            raise ValueError(Er)


class EnemiesConfigReader:
    def __init__(self):
        try:
            with open('configs/enemies_config.yaml', 'r') as file:
                enemies_config = yaml.safe_load(file)
        except Exception as Er:
            raise ValueError(Er)

        self.__conf = EnemiesConfig(**enemies_config)
        
    def get_characteristic(self, type_enemy: str) -> Dict:
        """Возвращает словарь характеристик врага без поля 'image'."""
        return self.__conf.get_characteristic(type_enemy)

    def get_path_image(self, type_enemy: str) -> str:
        """Возвращает путь к изображению врага из конфига."""
        return self.__conf.get_path_image(type_enemy)

if __name__ == '__main__':
    enemies = dict(enemies_characteristics={'basic': dict(image='images2d/enemy/common.png', health=3),
                'big': dict(image='images2d/enemy/armored_enemy.png', health=6),
                'regen': dict(image='images2d/enemy/regen.png', health=4, regen=2),
                'armored': dict(image='images2d/enemy/shield_enemy.png', health=3, armor=3),
                'invisible': dict(image='images2d/enemy/invisible.png', health=4, invisible=True),
                'giant': dict(image='images2d/enemy/giant.png', health=10)
                })

    yaml.dump(enemies, open('../../../../configs/enemies_config.yaml', 'w'), default_flow_style=False, sort_keys=False)
                
                