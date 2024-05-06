from dataclasses import dataclass

from oscartnetdaemon.entities.osc.configuration import OSCConfiguration
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    osc_configuration: OSCConfiguration = None
