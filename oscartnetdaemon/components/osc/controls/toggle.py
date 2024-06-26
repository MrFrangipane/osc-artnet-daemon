import logging
from typing import Any

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl
from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo
from oscartnetdaemon.components.domain.change_notification import ChangeNotification


_logger = logging.getLogger(__name__)


class OSCToggleControl(OSCAbstractControl):

    def __init__(self, info: OSCControlInfo, service: "OSCService"):
        super().__init__(info, service)
        self.components_singleton = Components  # FIXME
        self.value: bool = False

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def handle_osc(self, client_address, osc_address, osc_value):
        address_items = osc_address.split('/')

        if address_items[-1] == 'button':
            self.value = osc_value
            self.send_osc('/button', self.value)

    def handle_notification(self, change_notification: ChangeNotification):
        pass

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        return [
            ("/button", self.value),
            ("/caption", self.info.caption)
        ]

    def get_values(self) -> Any:
        return {'value': self.value}

    def set_values(self, values: Any):
        self.value = values['value']
        self.send_osc('/button', self.value)