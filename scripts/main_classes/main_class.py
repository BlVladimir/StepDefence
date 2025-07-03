from direct.showbase.ShowBase import ShowBase

from scripts.main_classes.context import Context


class StepDefence(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.__context = Context(self)