from scripts.main_classes.interface.context_interface import IContext


class KeyHandler:
    def __init__(self, accept, context:IContext):
        self.__accept = accept
        self.__accept("mouse1", lambda: self.on_left_click(context))

    @staticmethod
    def on_left_click(context:IContext):
        context.send_event(context.buttons_controller.action(context))