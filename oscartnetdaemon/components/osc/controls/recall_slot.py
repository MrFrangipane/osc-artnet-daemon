import logging
from typing import Any

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl
from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo
from oscartnetdaemon.components.domain.change_notification import ChangeNotification


_logger = logging.getLogger(__name__)


class OSCRecallSlotControl(OSCAbstractControl):

    def __init__(self, info: OSCControlInfo, service: "OSCService"):
        super().__init__(info, service)

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def handle_osc(self, client_address, osc_address, osc_value):
        subcontrol = osc_address.split('/')[-1]

        if osc_value == 1 and subcontrol == 'save':
            Components().osc_service.save_for_slot(self.info.osc_address)

        elif osc_value == 1 and subcontrol == 'recall':
            Components().osc_service.recall_for_slot(self.info.osc_address)

        elif subcontrol == 'punch':
            client_info = Components().osc_service.client_info_from_ip(client_address[0])
            Components().osc_service.set_punch_for_slot(client_info, self.info.osc_address, bool(osc_value))

    def handle_notification(self, change_notification: ChangeNotification):
        pass

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        return [
            ("/caption", self.info.caption)
        ]

    def get_values(self) -> Any:
        pass

    def set_values(self, values: Any):
        pass
