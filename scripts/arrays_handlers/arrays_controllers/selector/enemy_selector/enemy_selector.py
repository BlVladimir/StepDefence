from logging import error

from scripts.arrays_handlers.arrays_controllers.selector.abstract_selector import AbstractSelector
from scripts.arrays_handlers.arrays_controllers.selector.enemy_selector.attack_state import AttackState
from scripts.arrays_handlers.arrays_controllers.selector.enemy_selector.watch_state import WatchState
from scripts.main_classes.interaction.event_bus import EventBus


class EnemySelector(AbstractSelector):
    def __init__(self, define_enemy_set_func):
        super().__init__('watch', watch=WatchState(), attack=AttackState())
        self.__define_enemy_set_func = define_enemy_set_func

        EventBus.subscribe('using_tower', lambda event_type, data: self.change_state('attack', tower=data[0]))
        EventBus.subscribe('not_using_tower', lambda event_type, data: self.change_state('watch'))

    def change_state(self, state_name:str, **kwargs)->None:
        try:
            self._state_dict[self._current_state_name].not_used_state()
            self._current_state_name = state_name
            if state_name == 'attack':
                self._state_dict[state_name].use_state(**kwargs)
                self._state_dict[state_name].determine_set(self.__define_enemy_set_func())
        except KeyError:
            error('State not found')

