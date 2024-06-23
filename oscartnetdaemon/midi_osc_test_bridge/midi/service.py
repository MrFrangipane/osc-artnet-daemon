from queue import Empty, Queue
from threading import Thread

import mido

from oscartnetdaemon.midi_osc_test_bridge.domain.abstract_implementation import AbstractImplementation
from oscartnetdaemon.midi_osc_test_bridge.domain.change_notification import ChangeNotification
from oscartnetdaemon.midi_osc_test_bridge.midi.notification_origin import MIDINotificationOrigin


class MIDIService(AbstractImplementation):

    def start(self):
        print(mido.get_input_names())
        print(mido.get_output_names())
        self.input = mido.open_input('X-Touch 3')
        self.output = mido.open_output('X-Touch 4')

        self.out_messages = Queue()

        server_thread = Thread(target=self.loop, daemon=True)
        server_thread.start()

    def handle_change_notification(self, change_notification: ChangeNotification):
        value = int(change_notification.value * 16380.0 - 8192)
        self.out_messages.put(mido.Message('pitchwheel', channel=8, pitch=value))

    def loop(self):
        while True:
            in_message = self.input.receive(block=False)
            if in_message is not None:
                if in_message.channel == 8 and in_message.type == 'pitchwheel':
                    value = float(in_message.pitch + 8192) / 16380.0
                    self.domain.notify_change(ChangeNotification(
                        origin=MIDINotificationOrigin(),
                        control_name='FaderA',
                        value=value
                    ))

            while True:
                try:
                    message = self.out_messages.get(block=False)
                    if message is not None:
                        self.output.send(message)
                except Empty:
                    break
