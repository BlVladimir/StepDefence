from typing import Protocol, runtime_checkable

@runtime_checkable
class IRender(Protocol):
    @property
    def main_node3d(self):
        ...
    @property
    def loader(self):
        ...
    @property
    def main_node2d(self):
        ...
    @property
    def win(self):
        ...
    @property
    def convert_coordinate(self):
        ...
    def set_window_size(self, width, height):
        ... 