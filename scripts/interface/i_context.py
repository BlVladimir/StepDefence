from typing import Protocol, runtime_checkable

from scripts.main_classes.events.event_class import Event

@runtime_checkable
class IContext(Protocol):
    def send_event(self, event: Event)->None:
        ...

    @property
    def scene_controller(self)->'ISceneController':
        ...

    @property
    def render(self)->'IRenderManager':
        ...

    @property
    def key_watcher(self)->'IKeyWatcher':
        ...

    @property
    def settings(self)->'ISettings':
        ...

    @property
    def buttons_controller(self)->'IButtonsController':
        ...

    @property
    def task_mng(self)->'ITaskManager':
        ...