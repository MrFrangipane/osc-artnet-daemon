from dataclasses import dataclass

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.components.new_midi.io.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.new_midi.pagination_info import MIDIPaginationInfo


@dataclass
class MIDIConfiguration(BaseConfiguration):
    device_infos: dict[str, MIDIDeviceInfo]
    pagination_infos: dict[str, MIDIPaginationInfo]
