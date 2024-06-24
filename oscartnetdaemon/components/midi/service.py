from queue import Empty, Queue

import mido

from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.domain.control.float import FloatValue
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.midi.notification_origin import MIDINotificationOrigin
from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.midi.configuration_loader import load_midi_configuration


class MIDIService(AbstractImplementation):

    def __init__(self, configuration_info: ConfigurationInfo):
        super().__init__(configuration_info)
        self.midi_configuration = load_midi_configuration(self.configuration_info)
        self.midi_input: mido.ports.BaseInput = None
        self.midi_output: mido.ports.BaseOutput = None
        self.message_queue_out = None

    def initialize(self):
        print(mido.get_input_names())
        print(mido.get_output_names())

        self.midi_input = mido.open_input('X-Touch 4')
        self.midi_output = mido.open_output('X-Touch 5')

        self.message_queue_out = Queue()

    def poll_change_notification(self):
        while not self.in_notifications.empty():
            change_notification = self.in_notifications.get()
            value = int(change_notification.value.value * 16380.0 - 8192)
            self.message_queue_out.put(mido.Message('pitchwheel', channel=8, pitch=value))

    def exec(self):
        self.initialize()

        while True:
            in_message = self.midi_input.receive(block=False)
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
                    message = self.message_queue_out.get(block=False)
                    if message is not None:
                        self.midi_output.send(message)
                except Empty:
                    break

    def handle_termination(self):
        self.midi_input.close()
        self.midi_output.close()
