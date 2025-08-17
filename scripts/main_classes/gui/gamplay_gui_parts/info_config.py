from typing import Dict, List, Optional

import yaml


class InfoConfig:
    _instance: Optional['InfoConfig'] = None

    _tower_rus_info_dict:Dict[str, List[str]]

    @classmethod
    def load_config(cls)->None:
        try:
            with open('configs/info_config.yaml', 'r') as file:
                conf = yaml.safe_load(file)
        except Exception as Er:
            raise ValueError(Er)

        obj = cls()
        obj._tower_rus_info_dict = conf['towers_rus_info']
        cls._instance = obj


    @classmethod
    def get_tower_info(cls, tower_type:str)->List[str]:
        try:
            return cls._instance._tower_rus_info_dict[tower_type]
        except Exception as Er:
            raise ValueError(Er)

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
    })

    # Пишем файл в UTF-8 и разрешаем вывод кириллицы без \u-экранирования
    with open('../../../../configs/info_config.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(info, f, allow_unicode=True, sort_keys=False)