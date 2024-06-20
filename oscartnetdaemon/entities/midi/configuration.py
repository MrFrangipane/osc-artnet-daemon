from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo
from oscartnetdaemon.entities.midi.layer_group_info import MIDIControlLayerGroupInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIConfiguration:
    devices: dict[str, MIDIDeviceInfo]
    controls: dict[str, MIDIControlInfo]
    layer_groups: dict[str, MIDIControlLayerGroupInfo]
