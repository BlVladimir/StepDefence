from typing import Protocol, runtime_checkable

from scripts.interface.i_context import IContext


@runtime_checkable
class IKeyHandler(Protocol):
    @staticmethod
    def on_left_click(context: IContext):
        ... 