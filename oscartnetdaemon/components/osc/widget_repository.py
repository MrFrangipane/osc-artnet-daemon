from pythonosc.osc_server import Dispatcher

from oscartnetdaemon.components.osc.abstract_widget_repository import AbstractOSCWidgetRepository
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget
from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo
from oscartnetdaemon.entities.osc.widget_type_enum import OSCWidgetTypeEnum

from oscartnetdaemon.components.osc.widgets.color_wheel import OSCColorWheelWidget
from oscartnetdaemon.components.osc.widgets.fader import OSCFaderWidget
from oscartnetdaemon.components.osc.widgets.recall_slot import OSCRecallSlotWidget


class OSCWidgetRepository(AbstractOSCWidgetRepository):

    def __init__(self):
        self._widgets: list[OSCAbstractWidget] = list()

    def create_widgets(self, widget_infos: list[OSCWidgetInfo]) -> list[OSCAbstractWidget]:
        for widget_info in widget_infos:
            if widget_info.type == OSCWidgetTypeEnum.ColorWheel:
                new_widget = OSCColorWheelWidget(widget_info)
                self._widgets.append(new_widget)

            elif widget_info.type == OSCWidgetTypeEnum.Fader:
                new_widget = OSCFaderWidget(widget_info)
                self._widgets.append(new_widget)

            elif widget_info.type == OSCWidgetTypeEnum.RecallSlot:
                new_widget = OSCRecallSlotWidget(widget_info)
                self._widgets.append(new_widget)

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
            messages += widget.get_update_messages()
        return messages
