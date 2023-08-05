from collections import Mapping
from typing import Iterator


class Entity(Mapping):
    """
    This class provides the interface of Entity.

    An Entity is only a dictionary with the additional functionality of providing
    access to its items through __getattr__.
    """

    def __init__(self, data: Mapping):
        self.__data = data

    def __getitem__(self, k):
        return self.__data[k]

    def __len__(self) -> int:
        return len(self.__data)

    def __iter__(self) -> Iterator:
        return iter(self.__data)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def get(self, k, default=None):
        return self.__data.get(k, default)
