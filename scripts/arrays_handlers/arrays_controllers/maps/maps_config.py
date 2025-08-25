from typing import List, Dict, Optional
import yaml
from panda3d.core import Loader, Texture

from scripts.main_classes import rp


class MapsConfig:
    _instance: Optional['MapsConfig'] = None

    _keys: Dict
    _images_path: Dict
    _textures: Dict

    @classmethod
    def load_config(cls, loader:Loader) -> None:
        try:
            with open(rp.resource_path('configs/maps_config.yaml'), 'r', encoding='utf-8') as file:
                conf = yaml.safe_load(file)
        except Exception as Er:
            raise ValueError(Er)

        obj = cls()
        obj._keys = conf['keys']
        obj._images_path = conf['images_path']
        obj._textures = {tile: loader.loadTexture(conf['images_path'][tile]) for tile in conf['images_path'].keys()}

        cls._instance = obj

    @classmethod
    def get_map(cls, level:int)->List:
        try:
            return cls._instance._maps[level]
        except IndexError:
            raise ValueError(f'Level {level} not found')

    @classmethod
    def get_tile(cls, key:int)->str:
        try:
            return cls._instance._keys[key]
        except IndexError:
            raise ValueError(f'Key {key} not found')

    @classmethod
    def get_texture(cls, type_tile:str)->Texture:
        return cls._instance._textures[type_tile]

    @classmethod
    def get_all_keys(cls)->List:
        return list(cls._instance._keys.keys())