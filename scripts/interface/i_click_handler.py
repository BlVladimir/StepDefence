from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class ISelectedHandler(Protocol):
    def check_collision(self, task:Any)->Any:
        ... 