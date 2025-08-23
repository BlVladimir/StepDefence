from json import loads, dumps, dump
from os import makedirs, path


class SaveMng:
    _level:int

    @classmethod
    def load(cls):
        try:
            with open('saves/save.json', 'r', encoding='utf-8') as f:
                save_value = loads(f.read())
                cls._level = save_value['level']
        except Exception:
            cls._level = 0
            makedirs(path.dirname('saves/save.json'), exist_ok=True)
            with open('saves/save.json', 'w', encoding='utf-8') as f:
                dump({'level': 0}, f)

    @classmethod
    def save(cls, level:int):
        makedirs(path.dirname('saves/save.json'), exist_ok=True)
        with open('saves/save.json', 'w', encoding='utf-8') as f:
            dump({'level': level}, f)

    @classmethod
    def get_level(cls):
        return cls._level


if __name__ == '__main__':
    save = {'level':0}
    with open('../../saves/save.json', 'w', encoding='utf-8') as file:
        file.write(dumps(save))