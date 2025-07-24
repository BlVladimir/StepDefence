from typing import Callable

from direct.task import TaskManagerGlobal
from direct.task.Task import Task

from scripts.interface.i_task_manager import ITaskManager

class TaskManager(ITaskManager):

    def __init__(self, taskMng:TaskManagerGlobal):
        self.__taskMng = taskMng

    def append_task(self, name:str, task:Callable[[Task], Task]) -> None:
        self.__taskMng.add(task, name)

    def remove_task(self, name:str) -> None:
        self.__taskMng.remove(name)