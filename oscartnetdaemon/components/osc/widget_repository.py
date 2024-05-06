from pythonosc.osc_server import Dispatcher

from oscartnetdaemon.components.osc.abstract_widget_repository import AbstractOSCWidgetRepository
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget
from oscartnetdaemon.components.osc.widgets.color_wheel import OSCColorWheelWidget
from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo
from oscartnetdaemon.entities.osc.widget_type_enum import OSCWidgetTypeEnum


class OSCWidgetRepository(AbstractOSCWidgetRepository):

    def __init__(self):
        self._widgets: list[OSCAbstractWidget] = list()

    def create_widgets(self, widget_infos: list[OSCWidgetInfo]):
        for widget_info in widget_infos:
            if widget_info.type == OSCWidgetTypeEnum.ColorWheel:
                new_widget = OSCColorWheelWidget(widget_info)
                self._widgets.append(new_widget)

    def map_to_dispatcher(self, dispatcher: Dispatcher):
        for widget in self._widgets:
            dispatcher.map(
                widget.info.osc_address + '/*',
                widget.handle,
                needs_reply_address=True
            )
