from typing import List, Dict

from pydantic import BaseModel


class MapsConfig(BaseModel):
    maps: List
    keys: Dict
    images_path: Dict

    def get_map(self, level:int)->List:
        try:
            return self.maps[level]
        except IndexError:
            raise ValueError(f'Level {level} not found')

    def get_tile(self, key:int)->str:
        try:
            return self.keys[key]
        except IndexError:
            raise ValueError(f'Key {key} not found')

    def get_path(self, value:str)->str:
        try:
            return self.images_path[value]
        except IndexError:
            raise ValueError(f'Path {value} not found')

    def get_all_keys(self)->List:
        return list(self.keys.keys())