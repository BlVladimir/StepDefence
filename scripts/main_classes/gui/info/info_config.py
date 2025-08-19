from logging import error, debug
from typing import Dict, List, Optional

import yaml
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3


class InfoConfig:
    _instance: Optional['InfoConfig'] = None

    _towers_rus_info:Dict[str, List[str]]
    _enemies_rus_info:Dict[str, str]
    _effects_rus_info:Dict[str, str]

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
        cls._instance = obj


    @classmethod
    def get_tower_info(cls, tower_type:str)->List[str]:
        try:
            return cls._instance._towers_rus_info[tower_type]
        except Exception as Er:
            raise ValueError(Er)

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
            min_pt.x - left - xf,
            max_pt.x + right - xf,
            min_pt.z - bottom - zf,
            max_pt.z + top - zf
        ]
        return min_pt, max_pt, xf, zf

if __name__ == '__main__':
    info = dict(towers_rus_info={
        'basic': ['Дешёвая башня, способная\nдавать дополнительные 2\nмонеты за убийство.',
                  'Бонус за убийство\nсуммируется с тайлом.'],
        'sniper': ['Сильная башня, без эффектов.',
                   'Нет.'],
        'anty_shield': ['Игнорирует броню противника.',
                        'На бронибойном тайле не\nприобретает дополнительных\nэффектов.'],
        'venom': ['При ударе по врагу\nнакладывает эффект яда.',
                  'Яд игнорирует броню.\nТайл яда увеличит урон\nот яда на 1.'],
        'anty_invisible': ['Раскрывает невидимость\nврагов в своем радиусе.',
                           'На противоинвизном тайле\nне приобретает\nдополнительных эффектов.'],
        'cutter': ['Наносит урон всем врагам,\nкоторых пронизал его луч.',
                   'Игнорирует невидимость.'],
        'laser': ['Накладывает эффект лазер.\nОдновременно может наложить\nлазер только на одного врага.',
                  'Нет.'],
        'cannon': ['Бьёт в любую точку карты\nи наносит урон всем врагам\nв радиусе взрыва.',
                   'Игнорирует невидимость.\nТайл радиуса увеличит\nрадиус взрыва.']
    },
        enemies_rus_info=dict(basic='Обычный враг без эффектов.',
                              big='Враг с увеличенным количеством здоровья.',
                              regen='Каждый ход увеличивает свое здоровье.',
                              armored='Урон по врагу уменьшается на количество брони вплоть до 0.',
                              invisible='Радиус башен по этому врагу уменьшается в 3 раза. Не действует на сплэш-башни',
                              giant='Враг с огромным количеством здоровья.'),
        effects_rus_info=dict(
            poison='В конце каждого хода наносит урон, ад длительность уменьшается на 1. При нескольких эффектах яда наносится наибольший урон, но длительность уменьшается у всех эффектов.',
            laser='В конце каждого хода наносит урон. Каждый ход урон увеличивается на 1. Урон суммируется от всех лазеров.')
    )

    new_info = dict(towers_rus_info={
        'basic': ['Дешёвая башня, способная\nдавать дополнительные 2\nмонеты за убийство.',
                  'Бонус за убийство\nсуммируется с тайлом.'],
        'sniper': ['Сильная башня, без эффектов.'],
        'anty_shield': ['Игнорирует броню противника.',
                        'На бронибойном тайле не\nприобретает дополнительных\nэффектов.'],
        'venom': ['При ударе по врагу\nнакладывает эффект яда.',
                  'Яд игнорирует броню.\nТайл яда увеличит урон\nот яда на 1.'],
        'anty_invisible': ['Раскрывает невидимость\nврагов в своем радиусе.',
                           'На противоинвизном тайле\nне приобретает\nдополнительных эффектов.'],
        'cutter': ['Наносит урон всем врагам,\nкоторых пронизал его луч.',
                   'Игнорирует невидимость.'],
        'laser': ['Накладывает эффект лазер.\nОдновременно может наложить\nлазер только на одного врага.'],
        'cannon': ['Бьёт в любую точку карты\nи наносит урон всем врагам\nв радиусе взрыва.',
                   'Игнорирует невидимость.\nТайл радиуса увеличит\nрадиус взрыва.']
    },
        enemies_rus_info=dict(basic='Обычный враг без эффектов.',
                              big='Враг с увеличенным количеством здоровья.',
                              regen='Каждый ход увеличивает свое здоровье.',
                              armored='Урон по врагу уменьшается на количество брони вплоть до 0.',
                              invisible='Радиус башен по этому врагу уменьшается в 3 раза. Не действует на сплэш-башни',
                              giant='Враг с огромным количеством здоровья.'),
        effects_rus_info=dict(
            poison='В конце каждого хода наносит урон, ад длительность уменьшается на 1. При нескольких эффектах яда наносится наибольший урон, но длительность уменьшается у всех эффектов.',
            laser='В конце каждого хода наносит урон. Каждый ход урон увеличивается на 1. Урон суммируется от всех лазеров.')
    )

    # Пишем файл в UTF-8 и разрешаем вывод кириллицы без \u-экранирования
    with open('../../../../configs/info_config.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(new_info, f, allow_unicode=True, sort_keys=False)