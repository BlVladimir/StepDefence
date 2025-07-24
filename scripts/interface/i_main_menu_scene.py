from typing import Protocol, runtime_checkable

@runtime_checkable
class IMainMenuScene(Protocol):
    @staticmethod
    def name():
        ... 