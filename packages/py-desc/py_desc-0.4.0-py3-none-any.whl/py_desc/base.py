from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def __get__(self, instance, owner):
        pass

    @abstractmethod
    def __set__(self, instance, value):
        pass

    @abstractmethod
    def __set_name__(self, owner, name):
        pass
