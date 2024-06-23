from typing import Any

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.domain.abstract_service import AbstractDomainControlsService
from oscartnetdaemon.components.domain.entities.control_update_origin_enum import DomainControlUpdateOrigin
from oscartnetdaemon.components.domain.repository import DomainControlRepository


class DomainControlsService(AbstractDomainControlsService):
    def __init__(self):
        super().__init__()

    def start(self):
        self.control_repository = DomainControlRepository()
        self.control_repository.create_controls(Components().domain_controls_infos)

    def notify_update(self, origin: DomainControlUpdateOrigin, control_name: str, value: Any):
        self.control_repository.controls[control_name].set_value(value)

        if origin == DomainControlUpdateOrigin.OSC:
            pass
            # Components().midi_service.notify_update()
        else:
            Components().osc_service.notify_update(control_name, value)
