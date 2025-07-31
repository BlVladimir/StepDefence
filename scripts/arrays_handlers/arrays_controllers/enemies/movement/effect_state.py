from logging import error
from typing import List, Dict


class EffectState:
    """Состояние эффекта врага"""
    def __init__(self, effect_dict:Dict):
        self._effect_dict = effect_dict

    def get_effect_value(self, effect_name:str):
        if effect_name in self._effect_dict.keys():
            return self._effect_dict[effect_name]
        else:
            error('get_effect_value got incorrect effect name')
            return None

    def append_effect(self, effect_name:str, value:float|bool)->None:
        self._effect_dict[effect_name] = value

    def delete_effect(self, effect_name:str)->None:
        if effect_name in self._effect_dict.keys():
            del self._effect_dict[effect_name]
        else:
            error('delete_effect got incorrect effect name')