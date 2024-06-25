from dataclasses import dataclass

from oscartnetdaemon.components.domain.service import DomainService
from oscartnetdaemon.components.domain.entities.control_info import DomainControlInfo
from oscartnetdaemon.components.midi.service import MIDIService
# from oscartnetdaemon.components.midi.entities.configuration import MIDIConfiguration
# from oscartnetdaemon.components.osc.service import OSCService
# from oscartnetdaemon.components.osc.entities.configuration import OSCConfiguration
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass
from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration_info: ConfigurationInfo = None
    domain_control_infos: dict[str, DomainControlInfo] = None  # FIXME: make a DomainConfiguration dataclass ?
    domain_service: DomainService = None
    # midi_configuration: MIDIConfiguration = None
    # midi_service: MIDIService = None
    # osc_configuration: OSCConfiguration = None
    osc_service: AbstractImplementation = None
