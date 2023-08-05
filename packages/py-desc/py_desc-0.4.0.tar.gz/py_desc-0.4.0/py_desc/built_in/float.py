from typing import Union

from py_desc.base import Base


class PositiveFloat(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise ValueError('Must be float')
        if value < 0:
            raise ValueError('Cannot be negative')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class NegativeFloat(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise ValueError('Must be float')
        if value >= 0:
            raise ValueError('Cannot be positive')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class CustomFloat(Base):

    def __init__(self, first_value: Union[float, int] = None, last_value: Union[int, float] = None) -> None:
        if not (isinstance(first_value, (int, float)) and isinstance(last_value, (int, float))):
            if first_value is not None and last_value is not None:
                raise AttributeError('Cannot assign parameters for float field')
        if first_value is not None and last_value is not None:
            if first_value > last_value:
                raise AttributeError('Cannot assign last_value smaller then first_value')

        self.first_value = first_value
        self.last_value = last_value

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise ValueError('Must be float')

        if self.first_value is None and self.last_value is None:
            setattr(instance, self.name, value)
        elif self.first_value is None:
            if value >= self.last_value:
                raise ValueError(f'Cannot be equal or bigger than {self.last_value}')
        elif self.last_value is None:
            if value < self.first_value:
                raise ValueError(f'Cannot be smaller than {self.last_value}')
        else:
            if self.first_value <= value < self.last_value:
                setattr(instance, self.name, value)
            else:
                raise ValueError(f'Cannot be not in range [{self.first_value}:{self.last_value}]')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'
