from py_desc.base import Base


class SimpleTuple(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class TupleOfIntegers(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, int) for x in value]):
            raise ValueError('Values in tuple must be integers')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class TupleOfFloats(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, float) for x in value]):
            raise ValueError('Values in tuple must be float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class TupleOfNumbers(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, (int, float)) for x in value]):
            raise ValueError('Values in tuple must be integers or float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class TupleOfStrings(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, str) for x in value]):
            raise ValueError('Values in tuple must be strings')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class CustomTuple(Base):

    def __init__(self, classinfo: type):
        self.classinfo = classinfo

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, self.classinfo) for x in value]):
            raise ValueError(f'Values in tuple must be {self.classinfo}')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'
