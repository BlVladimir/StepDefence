from typing import Protocol, runtime_checkable

@runtime_checkable
class IStepDefence(Protocol):
    def _set_window_size(self, width, height):
        ...
    def spinCameraTask(self, task):
        ...
    def fixCameraTask(self, task):
        ... 