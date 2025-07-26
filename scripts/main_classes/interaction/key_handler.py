from collections.abc import Callable

from scripts.interface.i_context import IContext
from scripts.interface.i_key_handler import IKeyHandler


class KeyHandler(IKeyHandler):
    def __init__(self, accept:Callable, context:IContext):
        self.__accept = accept
        self.__accept("mouse1", lambda: self.on_left_click(context))

    @staticmethod
    def on_left_click(context:IContext):
        context.send_event(context.buttons_controller.action(context))
        context.scene_controller.send_using_selected_element()