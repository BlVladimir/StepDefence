from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class IClickHandler(Protocol):
    def check_tiles(self, task:Any)->Any:
        ... 