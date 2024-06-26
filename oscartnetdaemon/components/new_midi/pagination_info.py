from dataclasses import dataclass

from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo


@dataclass
class MIDIPaginationInfo:
    name: str
    page_count: int
    button_up: MIDIVariableInfo
    button_down: MIDIVariableInfo
    variables: list[list[MIDIVariableInfo]]
