from scripts.main_classes.context import Context


class KeyHandler:
    def __init__(self, accept, context:Context):
        self.__accept = accept
        self.__accept("mouse1", lambda: self.on_left_click(context))

    @staticmethod
    def on_left_click(context:Context):
        context.send_event(context.scene_controller.action(context))