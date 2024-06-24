from queue import Empty, Queue

import mido

from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.domain.control.float import FloatValue
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.midi.notification_origin import MIDINotificationOrigin


class MIDIService(AbstractImplementation):

    def __init__(self):
        super().__init__()
        self.input: mido.ports.BaseInput = None
        self.output: mido.ports.BaseOutput = None

        self.out_messages = None

    def initialize(self):
        print(mido.get_input_names())
        print(mido.get_output_names())

        self.input = mido.open_input('X-Touch 4')
        self.output = mido.open_output('X-Touch 5')

        self.out_messages = Queue()

    def poll_change_notification(self):
        while not self.in_notifications.empty():
            change_notification = self.in_notifications.get()
            value = int(change_notification.value.value * 16380.0 - 8192)
            self.out_messages.put(mido.Message('pitchwheel', channel=8, pitch=value))

    def exec(self):
        self.initialize()

        while True:
            in_message = self.input.receive(block=False)
            if in_message is not None:
                if in_message.channel == 8 and in_message.type == 'pitchwheel':
                    value = float(in_message.pitch + 8192) / 16380.0
                    self.out_notifications.put(ChangeNotification(
                        origin=MIDINotificationOrigin(),
                        control_name='octostrip',
                        value=FloatValue(value)
                    ))

            self.poll_change_notification()

            while True:
                try:
                    message = self.out_messages.get(block=False)
                    if message is not None:
                        self.output.send(message)
                except Empty:
                    break

    def handle_termination(self):
        self.input.close()
        self.output.close()
