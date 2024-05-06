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
        self.saturation = 0.0
        self.lightness = 0.0

    def handle(self, client_address, osc_address, osc_value):
        address_items = osc_address.split('/')
        root = '/'.join(address_items[:-1])

        if address_items[-1] == 'hue':
            self.hue = osc_value
            Components().osc_service.send_to_all_clients(root + '/hue', self.hue)

        elif address_items[-1] == 'saturation':
            self.saturation = osc_value
            Components().osc_service.send_to_all_clients(root + '/saturation', self.saturation)

        elif address_items[-1] == 'lightness':
            self.lightness = osc_value
            Components().osc_service.send_to_all_clients(root + '/lightness', self.lightness)

        r, g, b = map(lambda x: int(x * 255), colorsys.hls_to_rgb(self.hue, self.lightness, self.saturation))
        Components().osc_service.send_to_all_clients(root + '/color', f"{r:02x}{g:02x}{b:02x}")
