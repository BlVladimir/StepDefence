from typing import Callable

from direct.task import TaskManagerGlobal
from direct.task.Task import Task

from scripts.main_classes.interaction.event_bus import EventBus


class TaskManager:

    def __init__(self, taskMng:TaskManagerGlobal):
        self.__taskMng = taskMng
        EventBus.subscribe('append_task', lambda event_type, data: self.__append_task(data[0], data[1]))
        EventBus.subscribe('remove_task', lambda event_type, data: self.__remove_task(data))

    def __append_task(self, name:str, task:Callable[[Task], Task]) -> None:
        self.__taskMng.add(task, name)

    def __remove_task(self, name:str) -> None:
        self.__taskMng.remove(name)