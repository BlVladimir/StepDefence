from typing import Protocol, runtime_checkable

@runtime_checkable
class IKeyWatcher(Protocol):
    @property
    def mouse_watcher(self):
        ...
    @property
    def click_handler(self):
        ... 