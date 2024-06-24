from oscartnetdaemon.components.midi.controls.absolute import MIDIAbsoluteControl
from oscartnetdaemon.components.midi.controls.abstract import MIDIAbstractControl
from oscartnetdaemon.components.midi.controls.button import MIDIButtonControl
from oscartnetdaemon.components.midi.controls.toggle import MIDIToggleControl
from oscartnetdaemon.components.midi.entities.control_info import MIDIControlInfo
from oscartnetdaemon.components.midi.entities.control_type_enum import MIDIControlType
from oscartnetdaemon.components.midi.entities.context import MIDIContext


class MIDIControlRepository:

    def __init__(self):
        self.controls: dict[str, MIDIAbstractControl] = dict()
        self.mappings: dict[str, list[MIDIAbstractControl]] = dict()

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
                new_control = new_control_type(control_info)
                self.controls[control_info.name] = new_control
                if control_info.mapped_to:
                    if control_info.mapped_to not in self.mappings:
                        self.mappings[control_info.mapped_to] = [new_control]
                    else:
                        self.mappings[control_info.mapped_to].append(new_control)

        return self.controls

    def controls_from_mapping(self, mapped_to: str, context: MIDIContext) -> list[MIDIAbstractControl]:
        for control in self.mappings[mapped_to]:
            page_ok = control.info.page == -1 or control.info.page == context.current_page
            layer_ok = control.info.layer_name == "" or control.info.layer_name == context.current_layer.name
            if page_ok and layer_ok:
                yield control
