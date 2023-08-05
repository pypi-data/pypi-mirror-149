from py_desc.base import Base


class SimpleList(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError('Must be list')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class ListOfIntegers(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError('Must be list')
        if not all([isinstance(x, int) for x in value]):
            raise ValueError('Values in list must be integers')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class ListOfFloats(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError('Must be list')
        if not all([isinstance(x, float) for x in value]):
            raise ValueError('Values in list must be float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class ListOfNumbers(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError('Must be list')
        if not all([isinstance(x, (int, float)) for x in value]):
            raise ValueError('Values in list must be integers or float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class ListOfStrings(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError('Must be list')
        if not all([isinstance(x, str) for x in value]):
            raise ValueError('Values in list must be strings')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class CustomList(Base):

    def __init__(self, classinfo: type):
        self.classinfo = classinfo

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError('Must be list')
        if not all([isinstance(x, self.classinfo) for x in value]):
            raise ValueError(f'Values in list must be {self.classinfo}')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'
