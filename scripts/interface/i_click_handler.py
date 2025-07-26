from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class ISelectedHandler(Protocol):
    def check_tiles(self, task:Any)->Any:
        ... 