import colorsys
import logging
from typing import Any

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget
from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo


_logger = logging.getLogger(__name__)


class OSCColorWheelWidget(OSCAbstractWidget):

    def __init__(self, info: OSCWidgetInfo):
        super().__init__(info)
        self.components_singleton = Components  # FIXME
        self.hue = 0.0
        self.saturation = 1.0
        self.lightness = 0.5

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def handle(self, client_address, osc_address, osc_value):
        address_items = osc_address.split('/')

        if address_items[-1] == 'hue':
            self.hue = osc_value
            self.send_osc('/hue', self.hue)

        elif address_items[-1] == 'saturation':
            self.saturation = osc_value
            self.send_osc('/saturation', self.saturation)

        elif address_items[-1] == 'lightness':
            self.lightness = osc_value
            self.send_osc('/lightness', self.lightness)

        r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.hue, self.lightness, self.saturation))
        self.send_osc('/color', f"{r:02x}{g:02x}{b:02x}")

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.hue, self.lightness, self.saturation))
        return [
            ("/hue", self.hue),
            ("/saturation", self.saturation),
            ("/lightness", self.lightness),
            ("/color", f"{r:02x}{g:02x}{b:02x}"),
            ("/caption", self.info.caption)
        ]

    def set_values(self, values: Any):
        self.hue = values['hue']
        self.saturation = values['saturation']
        self.lightness = values['lightness']

        self.send_osc('/hue', self.hue)
        self.send_osc('/saturation', self.saturation)
        self.send_osc('/lightness', self.lightness)
        r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.hue, self.lightness, self.saturation))
        self.send_osc('/color', f"{r:02x}{g:02x}{b:02x}")

    def get_values(self) -> Any:
        return {
            'hue': self.hue,
            'saturation': self.saturation,
            'lightness': self.lightness
        }
