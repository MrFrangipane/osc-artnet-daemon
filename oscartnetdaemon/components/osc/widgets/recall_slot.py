import logging
from typing import Any

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget
from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo


_logger = logging.getLogger(__name__)


class OSCRecallSlotWidget(OSCAbstractWidget):

    def __init__(self, info: OSCWidgetInfo):
        super().__init__(info)

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def handle(self, client_address, osc_address, osc_value):
        subwidget = osc_address.split('/')[-1]

        if osc_value == 1 and subwidget == 'save':
            Components().osc_service.save_for_slot(self.info.osc_address)

        elif osc_value == 1 and subwidget == 'recall':
            Components().osc_service.recall_for_slot(self.info.osc_address)

        elif subwidget == 'punch':
            Components().osc_service.set_punch_for_slot(self.info.osc_address, bool(osc_value))

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        return [
            (self.info.osc_address + "/caption", self.info.caption)
        ]

    def get_values(self) -> Any:
        pass

    def set_values(self, values: Any):
        pass
