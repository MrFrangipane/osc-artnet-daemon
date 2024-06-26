import colorsys
import logging
from typing import Any

from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.domain.value.color import ColorValue
from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl
from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo

_logger = logging.getLogger(__name__)


class OSCColorWheelControl(OSCAbstractControl):

    def __init__(self, info: OSCControlInfo, service: "OSCService"):
        super().__init__(info, service)
        self.value: ColorValue = ColorValue()

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def handle_osc(self, client_address, osc_address, osc_value):
        pass
        # address_items = osc_address.split('/')
        #
        # if address_items[-1] == 'hue':
        #     self.hue = osc_value
        #     self.send_osc('/hue', self.hue)
        #
        # elif address_items[-1] == 'saturation':
        #     self.saturation = osc_value
        #     self.send_osc('/saturation', self.saturation)
        #
        # elif address_items[-1] == 'lightness':
        #     self.lightness = osc_value
        #     self.send_osc('/lightness', self.lightness)
        #
        # r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.value.h, self.value.l, self.value.s))
        # self.send_osc('/color', f"{r:02x}{g:02x}{b:02x}")

    def handle_notification(self, change_notification: ChangeNotification):
        pass

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.value.h, self.value.l, self.value.s))
        return [
            ("/hue", self.value.h),
            ("/saturation", self.value.s),
            ("/lightness", self.value.l),
            ("/color", f"{r:02x}{g:02x}{b:02x}"),
            ("/caption", self.info.caption)
        ]

    def set_values(self, values: Any):
        pass
        # self.hue = values['hue']
        # self.saturation = values['saturation']
        # self.lightness = values['lightness']
        #
        # self.send_osc('/hue', self.hue)
        # self.send_osc('/saturation', self.saturation)
        # self.send_osc('/lightness', self.lightness)
        # r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.value.h, self.value.l, self.value.s))
        # self.send_osc('/color', f"{r:02x}{g:02x}{b:02x}")

    def get_values(self) -> Any:
        return {
            'hue': self.value.h,
            'saturation': self.value.s,
            'lightness': self.value.l
        }
