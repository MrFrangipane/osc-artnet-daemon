from dataclasses import dataclass

from oscartnetdaemon.components.domain.abstract_service import AbstractDomainService
from oscartnetdaemon.components.midi.abstract_service import AbstractMidiService
from oscartnetdaemon.components.midi.entities.configuration import MIDIConfiguration
from oscartnetdaemon.components.osc.abstract_service import AbstractOSCService
from oscartnetdaemon.components.osc.entities.configuration import OSCConfiguration
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass
from oscartnetdaemon.components.domain.entities.control_info import DomainControlInfo


@dataclass
class Components(metaclass=SingletonMetaclass):
    domain_controls_infos: dict[str, DomainControlInfo] = None
    domain_service: AbstractDomainService = None
    midi_configuration: MIDIConfiguration = None
    midi_service: AbstractMidiService = None
    osc_configuration: OSCConfiguration = None
    osc_service: AbstractOSCService = None
