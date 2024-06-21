from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo
from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.layer_group_info import MIDIControlLayerGroupInfo
from oscartnetdaemon.entities.midi.pagination_info import MIDIPaginationInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIConfiguration:
    devices: dict[str, MIDIDeviceInfo]
    controls: dict[str, MIDIControlInfo]
    paginations: dict[str, MIDIPaginationInfo]
    layer_groups: dict[str, MIDIControlLayerGroupInfo]
