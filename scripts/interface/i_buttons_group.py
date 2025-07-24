from typing import Protocol, runtime_checkable

from scripts.interface.i_context import IContext


@runtime_checkable
class IButtonsGroup(Protocol):
    def action(self, context: IContext):
        ...
    def hide(self):
        ...
    def show(self):
        ... 