from logging import warning
from weakref import WeakSet

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.main_classes.interaction.event_bus import EventBus


class EnemiesManager:
    __enemies:WeakSet = WeakSet()

    def __init__(self):
        EventBus.subscribe('change_scene', lambda event_type, data: self.__warning())

    def __warning(self):
        if len(self.__enemies) > 0:
            warning(f'Enemies manager is not empty: len = {len(self.__enemies)}')

    def __add__(self, enemy:Enemy):
        self.__enemies.add(enemy)

    def __iter__(self):
        return iter(self.__enemies)

    def __len__(self):
        return len(self.__enemies)