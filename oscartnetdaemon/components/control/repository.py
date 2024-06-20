from oscartnetdaemon.components.control.controls.abstract_control import AbstractControl
from oscartnetdaemon.entities.control.control_info import ControlInfo
from oscartnetdaemon.entities.control.control_type_enum import ControlType


class ControlRepository:

    def __init__(self):
        self.controls: dict[str, AbstractControl] = dict()

    def create_controls(self, controls_infos: dict[str, ControlInfo]) -> dict[str, AbstractControl]:
        self.controls = dict()

        for control_info in controls_infos.values():
            new_control_type = {
                ControlType.Bool: AbstractControl,
                ControlType.Color: AbstractControl,
                ControlType.Float: AbstractControl,
                ControlType.String: AbstractControl
            }.get(control_info.type, None)

            if new_control_type is None:
                raise ValueError(f"Widget of type '{control_info.type.name}' does not exists")
            else:
                self.controls[control_info.name] = new_control_type(control_info)

        return self.controls
