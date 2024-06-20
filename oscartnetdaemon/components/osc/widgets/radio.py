import logging
from typing import Any

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget
from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo


_logger = logging.getLogger(__name__)


class OSCRadioWidget(OSCAbstractWidget):

    def __init__(self, info: OSCWidgetInfo):
        super().__init__(info)
        self.components_singleton = Components  # FIXME
        self.value: int = 0

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def on_change(self, client_address, osc_address, osc_value):
        address_items = osc_address.split('/')

        if address_items[-1] == 'radio':
            self.value = osc_value
            self.send_osc('/radio', self.value)

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        return [
            ("/radio", self.value),
            ("/caption", self.info.caption),
            ("/label1", self.info.labels[0]),
            ("/label2", self.info.labels[1]),
            ("/label3", self.info.labels[2]),
            ("/label4", self.info.labels[3]),
            ("/label5", self.info.labels[4])
        ]

    def get_values(self) -> Any:
        return {'value': self.value}

    def set_values(self, values: Any):
        self.value = values['value']
        self.send_osc('/radio', self.value)
