from typing import Protocol, runtime_checkable

@runtime_checkable
class ISettingsScene(Protocol):
    @staticmethod
    def name():
        ... 