from typing import Protocol, runtime_checkable

@runtime_checkable
class IScene(Protocol):
    @staticmethod
    def hide():
        ...
    @staticmethod
    def name() -> str:
        ... 