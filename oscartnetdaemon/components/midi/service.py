from multiprocessing import Queue

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.midi.configuration_loader import load_midi_configuration
from oscartnetdaemon.components.midi.control_repository import MIDIControlRepository
from oscartnetdaemon.components.midi.device import MIDIDevice
from oscartnetdaemon.components.midi.entities.context import MIDIContext
from oscartnetdaemon.components.midi.entities.message import MIDIMessage
from oscartnetdaemon.components.midi.message_handler import MIDIMessageHandler


class MIDIService(AbstractImplementation):

    def __init__(self, configuration_info: ConfigurationInfo):
        super().__init__(configuration_info)
        self.midi_configuration = load_midi_configuration(self.configuration_info)

        self.queue_in: Queue[MIDIMessage] = Queue()

        self.control_repository: MIDIControlRepository = None
        self.devices: dict[str, MIDIDevice] = None  # FIXME make a device repository ?
        self.message_handler: MIDIMessageHandler = None

    def initialize(self):
        self.control_repository = MIDIControlRepository()
        self.control_repository.create_controls(self.midi_configuration.controls.values())

        self.devices = dict()
        for device_info in self.midi_configuration.devices.values():
            self.devices[device_info.name] = MIDIDevice(device_info, self.queue_in, self.midi_configuration)
            self.devices[device_info.name].start()

        self.message_handler = MIDIMessageHandler(
            control_repository=self.control_repository,
            notification_queue=self.out_notifications
        )

        self.context = MIDIContext(
            current_page=0,
            current_layer=list(list(self.midi_configuration.layer_groups.values())[0].layers.values())[0]
        )

    def loop(self):
        while True:
            message = self.queue_in.get()
            self.message_handler.handle(message, self.context)
            self.poll_change_notification()

    def poll_change_notification(self):
        while not self.in_notifications.empty():
            change_notification = self.in_notifications.get()
            compliant_midi_controls = self.control_repository.controls_from_mapping(
                mapped_to=change_notification.control_name,
                context=self.context
            )
            for midi_control in compliant_midi_controls:
                midi_control.value = change_notification.value
                message = midi_control.make_message(midi_control.info.device)
                self.devices[midi_control.info.device.name].queue_out.put(message)

    def exec(self):
        self.initialize()
        self.loop()

    def handle_termination(self):
        for device in self.devices.values():
            device.stop()
