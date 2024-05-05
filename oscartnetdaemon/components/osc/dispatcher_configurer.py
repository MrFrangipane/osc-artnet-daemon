from pythonosc.dispatcher import Dispatcher

from oscartnetdaemon.components.osc.message_handler import OSCMessageHandler


class OSCDispatcherConfigurer:

    def __init__(self, message_handler: OSCMessageHandler):
        self.dispatcher: Dispatcher = Dispatcher()
        self._message_handler = message_handler

    def load(self, mappings):
        for mapping in mappings:
            if mapping['type'] == 'fader':
                self.dispatcher.map(
                    mapping['address'] + '/*',
                    self._message_handler.handle_fader,
                    needs_reply_address=True
                )

            elif mapping['type'] == 'palette_select':
                self.dispatcher.map(
                    mapping['address'] + '/*',
                    self._message_handler.handle_palette_select,
                    needs_reply_address=True
                )

            elif mapping['type'] == 'color_wheel':
                self.dispatcher.map(
                    mapping['address'] + '/*',
                    self._message_handler.handle_color_wheel,
                    needs_reply_address=True
                )

            elif mapping['type'] == 'recall_slot':
                self.dispatcher.map(
                    mapping['address'] + '/*',
                    self._message_handler.handle_recall_slot,
                    needs_reply_address=True
                )
        self.dispatcher.set_default_handler(self._message_handler.handle_default, needs_reply_address=True)
