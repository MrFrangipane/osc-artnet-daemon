from oscartnetdaemon.components.midi.controls.absolute import MIDIAbsoluteControl
from oscartnetdaemon.components.midi.controls.abstract import MIDIAbstractControl
from oscartnetdaemon.components.midi.controls.button import MIDIButtonControl
from oscartnetdaemon.components.midi.controls.toggle import MIDIToggleControl
from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo
from oscartnetdaemon.entities.midi.control_type_enum import MIDIControlType


class MIDIControlRepository:

    def __init__(self):
        self.controls: dict[str, MIDIAbstractControl] = dict()

    def create_controls(self, controls_infos: list[MIDIControlInfo]) -> dict[str, MIDIAbstractControl]:
        for control_info in controls_infos:
            new_control_type = {
                MIDIControlType.Absolute: MIDIAbsoluteControl,
                MIDIControlType.Button: MIDIButtonControl,
                MIDIControlType.Toggle: MIDIToggleControl
            }.get(control_info.type, None)

            if new_control_type is None:
                raise ValueError(f"Control of type '{control_info.type.name}' does not exists")
            else:
                self.controls[control_info.name] = new_control_type(control_info)

        return self.controls
