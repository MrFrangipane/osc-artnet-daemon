import logging
from typing import Any

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl
from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo
from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.osc.notification_origin import OSCNotificationOrigin
from oscartnetdaemon.components.domain.value.float import FloatValue


_logger = logging.getLogger(__name__)


class OSCFaderControl(OSCAbstractControl):

    def __init__(self, info: OSCControlInfo, service: "OSCService"):
        super().__init__(info, service)
        self.value: FloatValue = FloatValue()

    # fixme: return a list of message like in get_update_messages() ?
    # fixme: use a dataclass for messages ?
    def handle_osc(self, client_address, osc_address, osc_value):
        address_items = osc_address.split('/')

        if address_items[-1] == 'fader' and self.info.mapped_to:
            self.value.value = osc_value
            self.service.notifications_queue_out.put(ChangeNotification(
                control_name=self.info.mapped_to,
                value=self.value,
                origin=OSCNotificationOrigin(client_address[0])
            ))
            # self.value = osc_value
            # self.service.osc_messages_queue.put(('/fader', self.value))
            # self.service.osc_messages_queue.put(('/value', int(self.value * 255)))

    def handle_notification(self, change_notification: ChangeNotification):
        # print(change_notification)
        self.value = change_notification.value
        # self.service.osc_messages_queue.put(('/fader', self.value))
        # self.service.osc_messages_queue.put(('/value', int(self.value * 255)))

    # fixme: use a dataclass for messages ?
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        return [
            ("/fader", self.value.value),
            ("/value", int(self.value.value * 255)),
            ("/caption", self.info.caption)
        ]

    def get_values(self) -> Any:
        return {'value': self.value}

    def set_values(self, values: Any):
        self.value = values['value']
        self.service.osc_messages_queue.put(('/fader', self.value))
        self.service.osc_messages_queue.put(('/value', int(self.value * 255)))
