from typing import Protocol, runtime_checkable

@runtime_checkable
class IGameplayScene(Protocol):
    def create_scene(self, level):
        ...
    def close_scene(self):
        ...
    @staticmethod
    def name():
        ... 