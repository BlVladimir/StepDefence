from collections.abc import Callable
from itertools import product
from math import cos, sin
from random import choice
from typing import List, Iterator, Dict

from yaml import safe_dump, safe_load, dump


class LevelsConfig:
    _instance: 'LevelsConfig' = None
    _levels: Dict[int, Dict]
    __DEVELOPER_MONEY: int = 4000


    @classmethod
    def load_config(cls):
        with open('configs/levels.yaml', 'r', encoding='utf-8') as file:
            levels = safe_load(file)

        obj = cls()
        obj._levels = levels
        cls._instance = obj

    @classmethod
    def get_level_count_wave(cls, level:int)->int:
        return cls._instance._levels[level]['count_waves']

    @classmethod
    def get_level_towers(cls, level:int)->List[str]:
        return cls._instance._levels[level]['towers']

    @classmethod
    def get_level_money(cls, level:int)->int:
        return cls._instance._levels[level]['started_money'] if cls.__DEVELOPER_MONEY == 0 else cls.__DEVELOPER_MONEY

    @classmethod
    def get_level_enemies(cls, level:int, wave:int)->Dict:
        return cls._instance._levels[level]['waves'][wave]['enemies']

    @classmethod
    def get_level_health_k(cls, level:int, wave:int)->float:
        return cls._instance._levels[level]['waves'][wave]['health_k']+1

    @classmethod
    def get_level_map(cls, level:int)->List[List[int]]:
        return cls._instance._levels[level]['map']

if __name__ == '__main__':
    weight_dict = dict(basic=1, big=2, armored=2, regen=3, invisible=2, giant=3)
    f_health = lambda x, k: round((sin(2 * (x + 9)) + cos((x + 9)) + k * (x + 9) - 1)/2, 1)
    f_weight = lambda x: round(sin(2 * (x + 9)) + cos((x + 9)) + 4)

    def split_number(number:int, allowed:List[int])->List[List[int]]:
        return list(filter(lambda x: sum(x) == number,
                           [combo for k in range(2, 5) for combo in product(allowed, repeat=k)]))

    def dict_enm(enemies:List[str])->Dict[int, List[str]]:
        return {v: [k for k in enemies if weight_dict[k] == v]
                for v in set(weight_dict[k] for k in enemies)}

    def iter_enm_list(enemies:List[str], waves:int, choice_func:Callable, weight_func:Callable)->Iterator[List[List[str]]]:
        for wave in range(waves):
            yield [choice_func(dict_enm(enemies)[enm])
                   for enm in choice_func(split_number(weight_func(wave), list(dict_enm(enemies).keys())))]

    levels = {0:dict(count_waves=20,
                     towers=['basic', 'sniper'],
                     started_money=4,
                     waves=[dict(enemies=enms, health_k=f_health(hk, 0.3)) for hk, enms in enumerate(iter_enm_list(['basic', 'big'], 20, choice, f_weight))],
                     map=[[0, 3, 4, 4, 4],
                          [4, 1, 1, 1, 0],
                          [5, 0, 6, 1, 6],
                          [0, 1, 1, 1, 4],
                          [4, 2, 4, 0, 4]]),
              1: dict(count_waves=25,
                      towers=['basic', 'sniper', 'anty_shield'],
                      started_money=4,
                      waves=[dict(enemies=enms, health_k=f_health(hk, 0.3)) for hk, enms in
                             enumerate(iter_enm_list(['basic', 'big', 'armored'], 25, choice, f_weight))],
                      map=  [[3, 1, 1, 1, 4],
                             [4, 5, 4, 1, 4],
                             [1, 1, 1, 1, 0],
                             [1, 4, 0, 7, 0],
                             [2, 4, 6, 0, 0]]),
              2: dict(count_waves=30,
                      towers=['basic', 'sniper', 'anty_shield', 'venom'],
                      started_money=5,
                      waves=[dict(enemies=enms, health_k=f_health(hk, 0.3)) for hk, enms in
                             enumerate(iter_enm_list(['basic', 'big', 'armored', 'regen'], 30, choice, f_weight))],
                      map=[[0, 0, 0, 0, 0, 8, 0],
                           [0, 0, 4, 7, 1, 1, 3],
                           [0, 8, 5, 0, 1, 4, 0],
                           [2, 1, 4, 1, 1, 6, 0],
                           [4, 1, 1, 1, 4, 0, 0]]),
              3: dict(count_waves=35,
                      towers=['basic', 'sniper', 'anty_shield', 'venom', 'anty_invisible'],
                      started_money=5,
                      waves=[dict(enemies=enms, health_k=f_health(hk, 0.3)) for hk, enms in
                             enumerate(iter_enm_list(['basic', 'big', 'armored', 'regen', 'invisible'], 35, choice, f_weight))],
                      map=[[0, 4, 2, 0, 0, 0, 0],
                           [4, 1, 1, 4, 4, 6, 0],
                           [4, 1, 4, 1, 1, 0, 0],
                           [0, 1, 0, 3, 1, 0, 4],
                           [8, 1, 7, 0, 1, 4, 0],
                           [0, 1, 1, 1, 1, 4, 0],
                           [4, 0, 0, 5, 0, 0, 0]]),
              4: dict(count_waves=40,
                      towers=['basic', 'sniper', 'anty_shield', 'venom', 'anty_invisible', 'laser'],
                      started_money=6,
                      waves=[dict(enemies=enms, health_k=f_health(hk, 0.3)) for hk, enms in
                             enumerate(iter_enm_list(['basic', 'big', 'armored', 'regen', 'invisible', 'giant'], 40, choice, f_weight))],
                      map=[[0, 0, 0, 0, 4, 0, 0],
                           [4, 4, 0, 1, 1, 1, 0],
                           [0, 1, 1, 1, 0, 1, 8],
                           [4, 1, 4, 9, 0, 1, 4],
                           [5, 1, 0, 0, 0, 1, 4],
                           [0, 3, 0, 6, 7, 1, 2],
                           [0, 0, 0, 0, 0, 4, 0]]),
              5: dict(count_waves=40,
                      towers=['basic', 'sniper', 'anty_shield', 'venom', 'anty_invisible', 'laser', 'cutter', 'cannon'],
                      started_money=6,
                      waves=[dict(enemies=enms, health_k=f_health(hk, 0.3)) for hk, enms in
                             enumerate(iter_enm_list(['basic', 'big', 'armored', 'regen', 'invisible', 'giant'], 40, choice, f_weight))],
                      map=[[0, 0, 4, 0, 0, 4, 4],
                           [4, 1, 1, 1, 1, 1, 4],
                           [0, 3, 4, 0, 0, 1, 0],
                           [0, 0, 6, 0, 7, 1, 4],
                           [0, 4, 0, 8, 0, 1, 5],
                           [4, 0, 1, 1, 1, 1, 4],
                           [0, 4, 2, 0, 9, 0, 0]])
              }

    with open('../../configs/levels.yaml', 'w', encoding='utf-8') as file:
        safe_dump(levels, file, allow_unicode=True, sort_keys=False)