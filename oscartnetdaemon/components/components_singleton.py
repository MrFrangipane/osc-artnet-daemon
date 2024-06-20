from dataclasses import dataclass

from oscartnetdaemon.components.osc.abstract_service import AbstractOSCService
from oscartnetdaemon.entities.osc.configuration import OSCConfiguration
from oscartnetdaemon.components.control.abstract_service import AbstractControlsService
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    controls_infos: dict = None
    controls_service: AbstractControlsService = None
    osc_configuration: OSCConfiguration = None
    osc_service: AbstractOSCService = None
