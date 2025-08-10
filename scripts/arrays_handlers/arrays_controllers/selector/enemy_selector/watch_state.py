from typing import Optional

from scripts.arrays_handlers.arrays_controllers.selector.abstract_state_selector import AbstractStateSelector
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprite3D import Sprite3D


class WatchState(AbstractStateSelector):
    def __init__(self):
        super().__init__()

    def get_used_sprite(self)->Optional[Sprite3D]:
        """Когда нужно получить объект для использования"""
        if self._main_selected_sprite:
            EventBus.publish('draw_enemy_characteristic', self._main_selected_sprite.external_object.characteristic)
            self._main_selected_sprite.is_using = True
            return self._main_selected_sprite
        EventBus.publish('close_enemy_characteristic')
        return None