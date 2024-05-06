import logging

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget
from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo


_logger = logging.getLogger(__name__)


class OSCFaderWidget(OSCAbstractWidget):

    def __init__(self, info: OSCWidgetInfo):
        super().__init__(info)
        self.value: float = 0.5

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def handle(self, client_address, osc_address, osc_value):
        address_items = osc_address.split('/')

        if address_items[-1] == 'fader':
            self.value = osc_value
            Components().osc_service.send_to_all_clients(
                osc_address=self.info.osc_address + "/fader",
                osc_value=self.value
            )
            Components().osc_service.send_to_all_clients(
                osc_address=self.info.osc_address + "/value",
                osc_value=int(self.value * 255)
            )

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        return [
            (self.info.osc_address + "/fader", self.value),
            (self.info.osc_address + "/value", int(self.value * 255)),
            (self.info.osc_address + "/name", self.info.name)
        ]
