from logging import error, debug
from typing import Dict, List, Optional
from unittest import case

import yaml
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3


class InfoConfig:
    _instance: Optional['InfoConfig'] = None

    _towers_rus_info:Dict[str, List[str]]
    _enemies_rus_info:Dict[str, List[str]]
    _effects_rus_info:Dict[str, List[str]]
    _tiles_rus_info:Dict[str, List[str]]

    @classmethod
    def load_config(cls)->None:
        try:
            with open('configs/info_config.yaml', 'r') as file:
                conf = yaml.safe_load(file)
        except Exception as Er:
            raise ValueError(Er)

        obj = cls()
        obj._towers_rus_info = conf['towers_rus_info']
        obj._enemies_rus_info = conf['enemies_rus_info']
        obj._effects_rus_info = conf['effects_rus_info']
        obj._tiles_rus_info = conf['tiles_rus_info']
        cls._instance = obj


    @classmethod
    def get_obj_info(cls, type_obj:str, obj_name:str)->List[str]:
        try:
            match type_obj:
                case 'tower':
                    return cls._instance._towers_rus_info[obj_name]
                case 'enemy':
                    return cls._instance._enemies_rus_info[obj_name]
                case 'effect':
                    return cls._instance._effects_rus_info[obj_name]
                case 'tile':
                        return cls._instance._tiles_rus_info[obj_name]
                case _:
                    raise ValueError(f'Incorrect type:{type_obj}')
        except Exception as Er:
            raise ValueError(f'{Er}, {type_obj}, {obj_name}')

    @staticmethod
    def center_text(frame: DirectFrame | DirectButton, displacement_vec: Vec3 = Vec3(0, 0, 0)):
        try:
            text = frame.component('text0')
        except KeyError:
            error('text not found')
            return

        min_pt, max_pt = text.getTightBounds()

        x, z = frame['text_pos']

        frame['text_pos'] = (x + displacement_vec.x, z - (max_pt.z + min_pt.z) * 0.5 + displacement_vec.z)

    @staticmethod
    def set_frame(set_frame: DirectFrame, displacement_vec: Vec3 = Vec3(0, 0, 0), left=0.1, right=0.1, bottom=0.1,
                    top=0.1):
        """
        Центрирует текст в measure_frame и устанавливает frameSize у set_frame
        по измеренным tight bounds. Возвращает (min_pt, max_pt, xf, zf).
        Логику расчётов не меняем: используем pos того фрейма, у которого берём bounds.
        """
        InfoConfig.center_text(set_frame, displacement_vec)
        try:
            text = set_frame.component('text0')
        except KeyError:
            error('text not found')
            return None

        min_pt, max_pt = text.getTightBounds()
        vec_pos = set_frame['pos']
        xf, zf = vec_pos.x, vec_pos.z

        set_frame['frameSize'] = [
            min_pt.x - left,
            max_pt.x + right,
            min_pt.z - bottom,
            max_pt.z + top
        ]
        return min_pt, max_pt, xf, zf

if __name__ == '__main__':
    info = dict(towers_rus_info={
        'basic': dict(info=['Дешёвая башня, способная\nдавать дополнительные 2\nмонеты за убийство.',
                  'Бонус за убийство\nсуммируется с тайлом.'], links=[['tile', 'additional_money']]),
        'sniper': dict(info=['Сильная башня, без эффектов.']),
        'anty_shield': dict(info=['Игнорирует броню противника.',
                        'На бронибойном тайле не\nприобретает дополнительных\nэффектов.'], links=[['enemy', 'armored'], ['tile', 'armor_piercing']]),
        'venom': dict(info=['При ударе по врагу\nнакладывает эффект яда.',
                  'Яд игнорирует броню.\nТайл яда увеличит урон\nот яда на 1.'], links=[['effect', 'poison'], ['tile', 'poison']]),
        'anty_invisible': dict(info=['Раскрывает невидимость\nврагов в своем радиусе.',
                           'На противоинвизном тайле\nне приобретает\nдополнительных эффектов.'], links=[['enemy', 'invisible']]),
        'cutter': dict(info=['Наносит урон всем врагам,\nкоторых пронизал его луч.',
                   'Игнорирует невидимость.'], links=[['enemy', 'invisible']]),
        'laser': dict(info=['Накладывает эффект лазер.\nОдновременно может наложить\nлазер только на одного врага.'], links=[['effect', 'laser']]),
        'cannon': dict(info=['Бьёт в любую точку карты\nи наносит урон всем врагам\nв радиусе взрыва.',
                   'Игнорирует невидимость.\nТайл радиуса увеличит\nрадиус взрыва.'])
    },
        enemies_rus_info=dict(basic=dict(info=['Обычный враг без эффектов.']),
                              big=dict(info=['Враг с увеличенным\nколичеством здоровья.']),
                              regen=dict(info=['Каждый ход увеличивает\nсвое здоровье.'], links=[['tower', 'venom']]),
                              armored=dict(info=['Урон по врагу уменьшается\nна количество брони\nвплоть до 0.'], links=[['tower', 'anty_shield'], ['tile', 'armor_piercing']]),
                              invisible=dict(info=['Радиус башен по этому врагу\nуменьшается в 3 раза.\nНе действует на\nсплэш-башни'], links=[['tower', 'anty_invisible']]),
                              giant=dict(info=['Враг с огромным количеством\nздоровья.'])),
        effects_rus_info=dict(
            poison=dict(info=['В конце каждого хода наносит\nурон, а длительность\nуменьшается на 1.\nПри нескольких эффектах яда\nнаносится наибольший урон,\nно длительность уменьшается\nу всех эффектов.'], links=[['tower', 'venom'], ['tile', 'poison']]),
            laser=dict(info=['В конце каждого хода\nнаносит урон. Каждый ход\nурон увеличивается на 1.\nУрон суммируется от всех\nлазеров.'], links=[['tower', 'laser']]),),

        tiles_rus_info=dict(increase_damage=dict(info=['Увеличивает урон на 1']),
                        increase_radius=dict(info=['Увеличивает радиус в 1.5 раза']),
                        armor_piercing=dict(info=['Башня пробивает броню'], links=[['tower', 'anty_shield'], ['enemy', 'armored']]),
                        poison=dict(info=['Дает башне эффект яда'], links=[['tower', 'venom'], ['effect', 'poison']]),
                        additional_money=dict(info=['При убийстве 1 дополнительное золото'], links=[['tower', 'basic']]),)
    )

    # Пишем файл в UTF-8 и разрешаем вывод кириллицы без \u-экранирования
    with open('configs/info_config.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(info, f, allow_unicode=True, sort_keys=False)