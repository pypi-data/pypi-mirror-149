from py_desc.base import Base


class TrueBoolean(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError('Must be boolean')
        if not value:
            raise ValueError('Cannot be True')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'


class FalseBoolean(Base):

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError('Must be boolean')
        if value:
            raise ValueError('Cannot be True')
        setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f'_{name.lower()}'
