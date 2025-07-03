from direct.showbase.ShowBase import ShowBase

from scripts.main_classes.events.event_handler import EventHandler


class Context:
    def __init__(self, main_class:ShowBase):
        self.__event_handler = EventHandler
        pass