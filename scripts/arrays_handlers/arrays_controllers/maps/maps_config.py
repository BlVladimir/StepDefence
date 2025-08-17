from typing import List, Dict, Optional
import yaml


class MapsConfig:
    _instance: Optional['MapsConfig'] = None

    _maps: List
    _keys: Dict
    _images_path: Dict

    @classmethod
    def load_config(cls) -> None:
        try:
            with open('configs/maps_config.yaml', 'r') as file:
                conf = yaml.safe_load(file)
        except Exception as Er:
            raise ValueError(Er)

        obj = cls()
        obj._maps = conf['maps']
        obj._keys = conf['keys']
        obj._images_path = conf['images_path']

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
    def get_path(cls, value:str)->str:
        try:
            return cls._instance._images_path[value]
        except IndexError:
            raise ValueError(f'Path {value} not found')

    @classmethod
    def get_all_keys(cls)->List:
        return list(cls._instance._keys.keys())