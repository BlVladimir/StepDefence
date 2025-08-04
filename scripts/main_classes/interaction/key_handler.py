from collections.abc import Callable

from scripts.main_classes.interaction.event_bus import EventBus


class KeyHandler:
    def __init__(self, accept:Callable):
        self.__accept = accept
        self.__accept("mouse1", lambda: self.on_left_click())
        self.__accept("enter", lambda: self.on_enter_click())

    @staticmethod
    def on_left_click():
        EventBus.publish('right_click')

    @staticmethod
    def on_enter_click():
        EventBus.publish('next_round')