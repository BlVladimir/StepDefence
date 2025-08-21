from logging import info
from typing import Optional

from scripts.arrays_handlers.selector.abstract_state_selector import AbstractStateSelector
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprite3D import Sprite3D


class OneSelectedTileState(AbstractStateSelector):
    def __init__(self):
        super().__init__()

    def get_used_sprite(self) -> Optional[Sprite3D]:
        """Когда нужно получить объект для использования"""
        if self._main_selected_sprite:
            tower_node = self._main_selected_sprite.main_node.find('**/tower')
            if tower_node:
                tower = tower_node.getPythonTag('sprite').external_object
                tower.show_radius()
                EventBus.publish('using_tower', [tower, tower.level, tower.characteristic])
                info('tile with tower selected')
            elif self._main_selected_sprite.external_object.effect != 'road' and not tower_node:
                EventBus.publish('open_shop', self._main_selected_sprite.external_object.effect)
            self._main_selected_sprite.is_using = True
            return self._main_selected_sprite
        return None
