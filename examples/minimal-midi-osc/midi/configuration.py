from dataclasses import dataclass

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.components.midi.io.device_info import MIDIDeviceInfo


@dataclass
class MIDIConfiguration(BaseConfiguration):
    devices: dict[str, MIDIDeviceInfo]
