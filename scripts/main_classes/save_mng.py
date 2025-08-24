from json import loads, dumps, dump

from scripts.main_classes import rp


class SaveMng:
    _level:int

    @classmethod
    def load(cls):
        try:
            with open(rp.resource_path('saves/save.json'), 'r', encoding='utf-8') as f:
                save_value = loads(f.read())
                cls._level = save_value['level']
        except Exception:
            raise ValueError('Error in load save')

    @classmethod
    def save(cls, level:int):
        with open(rp.resource_path('saves/save.json'), 'w', encoding='utf-8') as f:
            dump({'level': level}, f)

    @classmethod
    def get_level(cls):
        return cls._level


if __name__ == '__main__':
    save = {'level':0}
    with open('../../saves/save.json', 'w', encoding='utf-8') as file:
        file.write(dumps(save))