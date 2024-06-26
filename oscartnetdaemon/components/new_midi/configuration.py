from dataclasses import dataclass

from oscartnetdaemon.components.new_midi.io.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.new_midi.layer_group_info import MIDILayerGroupInfo
from oscartnetdaemon.components.new_midi.pagination_info import MIDIPaginationInfo
from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration


@dataclass
class MIDIConfiguration(BaseConfiguration):
    device_infos: dict[str, MIDIDeviceInfo]
    pagination_infos: dict[str, MIDIPaginationInfo]
    layer_group_infos: dict[str, MIDILayerGroupInfo]
