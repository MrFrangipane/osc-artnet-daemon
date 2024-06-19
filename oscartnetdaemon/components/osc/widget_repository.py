from pythonosc.osc_server import Dispatcher

from oscartnetdaemon.components.osc.abstract_widget_repository import AbstractOSCWidgetRepository
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget
from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo
from oscartnetdaemon.entities.osc.widget_type_enum import OSCWidgetTypeEnum

from oscartnetdaemon.components.osc.widgets.button import OSCButtonWidget
from oscartnetdaemon.components.osc.widgets.color_wheel import OSCColorWheelWidget
from oscartnetdaemon.components.osc.widgets.fader import OSCFaderWidget
from oscartnetdaemon.components.osc.widgets.radio import OSCRadioWidget
from oscartnetdaemon.components.osc.widgets.recall_slot import OSCRecallSlotWidget
from oscartnetdaemon.components.osc.widgets.toggle import OSCToggleWidget


class OSCWidgetRepository(AbstractOSCWidgetRepository):

    def __init__(self):
        self._widgets: list[OSCAbstractWidget] = list()

    def create_widgets(self, widget_infos: list[OSCWidgetInfo]) -> list[OSCAbstractWidget]:
        for widget_info in widget_infos:
            new_widget_type = {
                OSCWidgetTypeEnum.Button: OSCButtonWidget,
                OSCWidgetTypeEnum.ColorWheel: OSCColorWheelWidget,
                OSCWidgetTypeEnum.Fader: OSCFaderWidget,
                OSCWidgetTypeEnum.Radio: OSCRadioWidget,
                OSCWidgetTypeEnum.RecallSlot: OSCRecallSlotWidget,
                OSCWidgetTypeEnum.Toggle: OSCToggleWidget
            }.get(widget_info.type, None)

            if new_widget_type is None:
                raise ValueError(f"Widget of type '{widget_info.type.name}' does not exists")
            else:
                self._widgets.append(new_widget_type(widget_info))

        return self._widgets

    def map_to_dispatcher(self, dispatcher: Dispatcher):
        for widget in self._widgets:
            dispatcher.map(
                widget.info.osc_address + '/*',
                widget.handle,
                needs_reply_address=True
            )

    def get_all_widget_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        messages = list()
        for widget in self._widgets:
            for address, value in widget.get_update_messages():
                messages.append((widget.info.osc_address + address, value))
        return messages
