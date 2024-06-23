from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.midi.entities.control_info import MIDIControlInfo
from oscartnetdaemon.components.midi.entities.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.entities.layer_group_info import MIDIControlLayerGroupInfo
from oscartnetdaemon.components.midi.entities.pagination_info import MIDIPaginationInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIConfiguration:
    devices: dict[str, MIDIDeviceInfo]
    controls: dict[str, MIDIControlInfo]
    paginations: dict[str, MIDIPaginationInfo]
    layer_groups: dict[str, MIDIControlLayerGroupInfo]
