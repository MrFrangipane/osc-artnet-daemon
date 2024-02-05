from dataclasses import dataclass

from oscartnet.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Configuration(metaclass=SingletonMetaclass):
    pass
