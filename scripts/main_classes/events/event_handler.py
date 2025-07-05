from scripts.main_classes.events.event_class import Event

class EventHandler:
    """Направляет событие нужному классу"""
    @staticmethod
    def handle_event(event:Event, context):
        """Обработка событий"""
        match event.name:
            case 'change_scene':
                context.scene_controller.change_scene(event)