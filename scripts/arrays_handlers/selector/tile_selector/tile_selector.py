from logging import error
from typing import Optional

from scripts.arrays_handlers.selector.abstract_selector import AbstractSelector
from scripts.arrays_handlers.selector.tile_selector.one_selected_tile_state import \
    OneSelectedTileState
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.main_classes.interaction.event_bus import EventBus


class TileSelector(AbstractSelector):
    def __init__(self):
        super().__init__('one_tile', one_tile = OneSelectedTileState())

    def set_used_sprite(self) -> None:
        try:
            if tower := self.used_tower:
                tower.hide_radius()
                EventBus.publish('not_using_tower')
                self._used_sprite.is_using = False
            elif self._used_sprite and self._used_sprite.external_object.effect != 'road':
                EventBus.publish('close_shop')
                self._used_sprite.is_using = False
            elif self._used_sprite:
                self._used_sprite.is_using= False
            self._used_sprite = self._state_dict[self._current_state_name].get_used_sprite()
            self._state_dict[self._current_state_name].unselect_sprite()
        except KeyError:
            error('State not found')

    @property
    def used_tower(self)->Optional[Tower]:
        if self._used_sprite and self._used_sprite.main_node.find('**/tower'):
            return self._used_sprite.main_node.find('**/tower').getPythonTag('sprite').external_object
        return None
