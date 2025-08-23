from logging import warning
from typing import Any
from weakref import WeakSet

from scripts.main_classes.interaction.event_bus import EventBus


class ObjectsManager:
    def __init__(self):
        self.__objects: WeakSet = WeakSet()
        EventBus.subscribe('change_scene', lambda event_type, data: self.__warning(data))

    def __warning(self, scene:str):
        if scene in '012345' and len(self.__objects) > 0:
            warning(f'Object manager is not empty: len = {len(self.__objects)}')

    def __add__(self, new_object:Any):
        self.__objects.add(new_object)

    def __iter__(self):
        return iter(self.__objects)

    def __len__(self):
        return len(self.__objects)