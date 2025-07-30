from scripts.main_classes.events.event_class import Event
from scripts.interface.i_event_handler import IEventHandler

class EventHandler(IEventHandler):
    """Направляет событие нужному классу"""
    @staticmethod
    def handle_event(event:Event, context):
        """Обработка событий"""
        match event.name:
            case 'change_scene':
                context.scene_controller.change_scene(event, context)
                context.buttons_controller.vision_control(context)
            case 'buy_tower':
                context.scene_controller.create_tower_on_current_tile(event['type'])
                context.buttons_controller.close_shop()