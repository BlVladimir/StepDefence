from typing import Protocol, runtime_checkable

@runtime_checkable
class IClickHandler(Protocol):
    def check_tiles(self):
        ... 