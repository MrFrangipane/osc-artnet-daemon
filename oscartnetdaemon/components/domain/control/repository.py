from oscartnetdaemon.components.domain.control.abstract import AbstractDomainControl
from oscartnetdaemon.components.domain.control.color import ColorControl
from oscartnetdaemon.components.domain.control.float import FloatControl
from oscartnetdaemon.components.domain.entities.control_info import DomainControlInfo
from oscartnetdaemon.components.domain.entities.control_type_enum import DomainControlType


class DomainControlRepository:

    def __init__(self):
        self.controls: dict[str, AbstractDomainControl] = dict()

    def create_controls(self, controls_infos: dict[str, DomainControlInfo]) -> dict[str, AbstractDomainControl]:
        self.controls = dict()

        for control_info in controls_infos.values():
            new_control_type = {
                DomainControlType.Bool: AbstractDomainControl,
                DomainControlType.Color: ColorControl,
                DomainControlType.Float: FloatControl,
                DomainControlType.String: AbstractDomainControl
            }.get(control_info.type, None)

            if new_control_type is None:
                raise ValueError(f"Control of type '{control_info.type.name}' does not exists")
            else:
                self.controls[control_info.name] = new_control_type(control_info)

        return self.controls
