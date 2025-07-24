from typing import Protocol, runtime_checkable

from scripts.interface.i_context import IContext
from scripts.main_classes.events.event_class import Event


@runtime_checkable
class IButtonsController(Protocol):
    def action(self, context: IContext)->Event:
        ...

    def vision_control(self, context: IContext)->None:
        ...