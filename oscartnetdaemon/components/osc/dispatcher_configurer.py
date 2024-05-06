from pythonosc.dispatcher import Dispatcher

from oscartnetdaemon.components.osc.message_handler import OSCMessageHandler
from oscartnetdaemon.entities.osc.widget import OSCWidget
from oscartnetdaemon.entities.osc.widget_type_enum import OSCWidgetTypeEnum


class OSCDispatcherConfigurer:

    def __init__(self, message_handler: OSCMessageHandler):
        self.dispatcher: Dispatcher = Dispatcher()
        self._message_handler = message_handler

    def load(self, widgets: list[OSCWidget]):
        for widget in widgets:
            if widget.type == OSCWidgetTypeEnum.Fader:
                self.dispatcher.map(
                    widget.osc_address + '/*',
                    self._message_handler.handle_fader,
                    needs_reply_address=True
                )

            elif widget.type == OSCWidgetTypeEnum.PaletteSelect:
                self.dispatcher.map(
                    widget.osc_address + '/*',
                    self._message_handler.handle_palette_select,
                    needs_reply_address=True
                )

            elif widget.type == OSCWidgetTypeEnum.ColorWheel:
                self.dispatcher.map(
                    widget.osc_address + '/*',
                    self._message_handler.handle_color_wheel,
                    needs_reply_address=True
                )

            elif widget.type == OSCWidgetTypeEnum.RecallSlot:
                self.dispatcher.map(
                    widget.osc_address + '/*',
                    self._message_handler.handle_recall_slot,
                    needs_reply_address=True
                )
        self.dispatcher.set_default_handler(self._message_handler.handle_default, needs_reply_address=True)
