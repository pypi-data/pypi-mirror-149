from py_desc.base import Base


class SimpleSet(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, set):
            raise ValueError('Must be set')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class SetOfIntegers(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, int) for x in value]):
            raise ValueError('Values in set must be integers')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class SetOfFloats(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, float) for x in value]):
            raise ValueError('Values in set must be float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class SetOfNumbers(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, (int, float)) for x in value]):
            raise ValueError('Values in set must be integers or float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class SetOfStrings(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, str) for x in value]):
            raise ValueError('Values in set must be strings')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class CustomSet(Base):

    def __init__(self, classinfo: type):
        self.classinfo = classinfo

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, self.classinfo) for x in value]):
            raise ValueError(f'Values in set must be {self.classinfo}')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'
