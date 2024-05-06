import colorsys
import logging

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget
from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo


_logger = logging.getLogger(__name__)


class OSCColorWheelWidget(OSCAbstractWidget):

    def __init__(self, info: OSCWidgetInfo):
        super().__init__(info)
        self.hue = 0.0
        self.saturation = 1.0
        self.lightness = 0.5

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def handle(self, client_address, osc_address, osc_value):
        address_items = osc_address.split('/')

        if address_items[-1] == 'hue':
            self.hue = osc_value
            Components().osc_service.send_to_all_clients(
                osc_address=self.info.osc_address + '/hue',
                osc_value=self.hue
            )

        elif address_items[-1] == 'saturation':
            self.saturation = osc_value
            Components().osc_service.send_to_all_clients(
                osc_address=self.info.osc_address + '/saturation',
                osc_value=self.saturation
            )

        elif address_items[-1] == 'lightness':
            self.lightness = osc_value
            Components().osc_service.send_to_all_clients(
                osc_address=self.info.osc_address + '/lightness',
                osc_value=self.lightness
            )

        r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.hue, self.lightness, self.saturation))
        Components().osc_service.send_to_all_clients(
            osc_address=self.info.osc_address + '/color',
            osc_value=f"{r:02x}{g:02x}{b:02x}"
        )

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.hue, self.lightness, self.saturation))
        return [
            (self.info.osc_address + "/hue", self.hue),
            (self.info.osc_address + "/saturation", self.saturation),
            (self.info.osc_address + "/lightness", self.lightness),
            (self.info.osc_address + "/color", f"{r:02x}{g:02x}{b:02x}"),
            (self.info.osc_address + "/name", self.info.name)
        ]
