from collections.abc import Mapping

class Event(Mapping):
    def __init__(self, name, **attributes):
        self.__name = name
        self.__attributes = attributes

    def __str__(self):
        return self.__name

    def __getitem__(self, item):
        try:
            return self.__attributes[item]
        except:
            raise Exception('Non-existent event key')

    def __iter__(self):
        return iter(self.__attributes)

    def __len__(self):
        return len(self.__attributes)

if __name__ == '__main__':
    a = Event('aga', a=1, b=2)
    print(a)

    for key in a:
        print(a[key])
