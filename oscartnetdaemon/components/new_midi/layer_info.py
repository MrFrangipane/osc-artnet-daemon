from dataclasses import dataclass

from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo


@dataclass
class MIDILayerInfo:
    name: str
    button_activate: MIDIVariableInfo
    variables: list[MIDIVariableInfo]
