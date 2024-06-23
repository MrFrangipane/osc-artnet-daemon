from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.midi.entities.layer_info import MIDIControlLayerInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlLayerGroupInfo:
    name: str
    layers: dict[str, MIDIControlLayerInfo]
