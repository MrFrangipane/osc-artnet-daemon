from typing import Any
from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.control.repository import ControlRepository
from oscartnetdaemon.components.control.abstract_service import AbstractControlsService
from oscartnetdaemon.entities.control.control_update_origin_enum import ControlUpdateOrigin


class ControlsService(AbstractControlsService):
    def __init__(self):
        super().__init__()

    def start(self):
        self.control_repository = ControlRepository()
        self.control_repository.create_controls(Components().controls_infos)

    def notify_update(self, origin: ControlUpdateOrigin, control_name: str, value: Any):
        self.control_repository.controls[control_name].set_value(value)

        if origin == ControlUpdateOrigin.OSC:
            pass
            # Components().midi_service.notify_update()
        else:
            Components().osc_service.notify_update(control_name, value)
