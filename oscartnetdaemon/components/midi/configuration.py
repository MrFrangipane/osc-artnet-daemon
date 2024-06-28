from dataclasses import dataclass

from oscartnetdaemon.components.midi.io.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.layer_group_info import MIDILayerGroupInfo
from oscartnetdaemon.components.midi.pagination_info import MIDIPaginationInfo
from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration


@dataclass
class MIDIConfiguration(BaseConfiguration):
    device_infos: dict[str, MIDIDeviceInfo]
    pagination_infos: dict[str, MIDIPaginationInfo]
    layer_group_infos: dict[str, MIDILayerGroupInfo]
