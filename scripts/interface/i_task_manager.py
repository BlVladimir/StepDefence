from typing import Protocol, runtime_checkable, Callable
from direct.task.Task import Task


@runtime_checkable
class ITaskManager(Protocol):
    def append_task(self, name:str, task:Callable) -> None:
        ...

    def remove_task(self, name:str) -> None:
        ...
    