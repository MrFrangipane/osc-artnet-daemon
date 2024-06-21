from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo
from oscartnetdaemon.entities.midi.layer_info import MIDIControlLayerInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlLayerGroupInfo:
    name: str
    layers: dict[str, MIDIControlLayerInfo]
