# Singleton class - inherit it for only a single object of a given class to exist
from abc import ABC


class Singleton(ABC):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
