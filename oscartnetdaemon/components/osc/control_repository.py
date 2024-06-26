from pythonosc.osc_server import Dispatcher

from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl
from oscartnetdaemon.components.osc.controls.fader import OSCFaderControl
from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo
from oscartnetdaemon.components.osc.entities.control_type_enum import OSCControlType


class OSCControlRepository:

    def __init__(self, service: "OSCService"):
        self.service = service
        self._controls: list[OSCAbstractControl] = list()

    def create_controls(self, controls_infos: list[OSCControlInfo]) -> list[OSCAbstractControl]:
        for control_info in controls_infos:
            new_control_type = {
                OSCControlType.Fader: OSCFaderControl
            }.get(control_info.type, None)

            if new_control_type is None:
                raise ValueError(f"Control of type '{control_info.type.name}' does not exists")
            else:
                self._controls.append(new_control_type(control_info, self.service))

        return self._controls

    def map_to_dispatcher(self, dispatcher: Dispatcher):
        for control in self._controls:
            dispatcher.map(
                control.info.osc_address + '/*',
                control.handle_osc,
                needs_reply_address=True
            )

    def get_all_controls_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        messages = list()
        for control in self._controls:
            for address, value in control.get_update_messages():
                messages.append((control.info.osc_address + address, value))
        return messages

    def control_from_mapping(self, control_name: str) -> None | OSCAbstractControl:
        for control in self._controls:
            if control.info.mapped_to == control_name:
                return control

    def forward_notification(self, change_notification: ChangeNotification):
        for control in self._controls:
            if control.info.mapped_to == change_notification.control_name:
                control.handle_notification(change_notification)
