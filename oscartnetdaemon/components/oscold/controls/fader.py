import logging
from typing import Any

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl
from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo


_logger = logging.getLogger(__name__)


class OSCFaderControl(OSCAbstractControl):

    def __init__(self, info: OSCControlInfo):
        super().__init__(info)
        self.components_singleton = Components  # FIXME
        self.value: float = 0.5

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def on_change(self, client_address, osc_address, osc_value):
        address_items = osc_address.split('/')

        if address_items[-1] == 'fader':
            self.value = osc_value
            self.send_osc('/fader', self.value)
            self.send_osc('/value', int(self.value * 255))

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        return [
            ("/fader", self.value),
            ("/value", int(self.value * 255)),
            ("/caption", self.info.caption)
        ]

    def get_values(self) -> Any:
        return {'value': self.value}

    def set_values(self, values: Any):
        self.value = values['value']
        self.send_osc('/fader', self.value)
        self.send_osc('/value', int(self.value * 255))
