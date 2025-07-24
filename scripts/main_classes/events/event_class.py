from typing import Any, Iterator
from collections.abc import Mapping

class Event(Mapping):
    """Событие"""
    def __init__(self, name: str, **attributes: Any) -> None:
        self._name: str = name
        self.__attributes: dict[str, Any] = attributes

    def __str__(self) -> str:
        return self._name

    def __getitem__(self, item: str) -> Any:
        try:
            return self.__attributes[item]
        except Exception:
            raise Exception('Non-existent event key')

    def __iter__(self) -> Iterator[str]:
        return iter(self.__attributes)

    def __len__(self) -> int:
        return len(self.__attributes)

    @property
    def name(self) -> str:
        return self._name

if __name__ == '__main__':
    a = Event('aga', a=1, b=2)
    print(a)

    for key in a:
        print(a[key])
