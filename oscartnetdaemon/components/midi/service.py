from multiprocessing import Queue

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.midi.configuration_loader import load_midi_configuration
from oscartnetdaemon.components.midi.control_repository import MIDIControlRepository
from oscartnetdaemon.components.midi.device import MIDIDevice
from oscartnetdaemon.components.midi.entities.context import MIDIContext
from oscartnetdaemon.components.midi.entities.message import MIDIMessage
from oscartnetdaemon.components.midi.notification_origin import MIDINotificationOrigin


class MIDIService(AbstractImplementation):

    def __init__(self, configuration_info: ConfigurationInfo):
        super().__init__(configuration_info)
        self.midi_configuration = load_midi_configuration(self.configuration_info)

        self.queue_midi_in: Queue[MIDIMessage] = Queue()

        self.control_repository: MIDIControlRepository = None
        self.devices: dict[str, MIDIDevice] = None  # FIXME make a device repository ?
        self.context: MIDIContext = None

    def exec(self):
        self.initialize()
        self.loop()

    def initialize(self):
        self.control_repository = MIDIControlRepository()
        self.control_repository.create_controls(self.midi_configuration.controls.values())

        self.devices = dict()
        for device_info in self.midi_configuration.devices.values():
            self.devices[device_info.name] = MIDIDevice(device_info, self.queue_midi_in, self.midi_configuration)
            self.devices[device_info.name].start()

        # FIXME: don't assume there's only one pagination and one layer group
        first_layer = list(list(self.midi_configuration.layer_groups.values())[0].layers.values())[0]
        self.context = MIDIContext(
            current_page=0,
            current_layer=first_layer
        )

    def loop(self):
        while True:
            while not self.queue_midi_in.empty():
                message = self.queue_midi_in.get()
                self.handle_message(message)

            self.poll_change_notification()

    def poll_change_notification(self):
        while not self.notification_queue_in.empty():
            change_notification = self.notification_queue_in.get()

            # Forward to controls
            mapped_midi_controls = self.control_repository.controls_from_mapping(
                mapped_to=change_notification.control_name,
                context=self.context
            )
            for midi_control in mapped_midi_controls:
                midi_control.value = change_notification.value
                message = midi_control.make_message(midi_control.info.device)
                self.devices[midi_control.info.device.name].queue_out.put(message)

    def handle_termination(self):
        for device in self.devices.values():
            device.stop()

    def handle_message(self, message: MIDIMessage):
        for midi_control in self.control_repository.controls.values():
            if midi_control.complies_with(message, self.context) and midi_control.handle_message(message, self.context):
                print(midi_control.info, midi_control.value)

                #
                # Mapped to domain
                if midi_control.info.mapped_to:
                    self.notifications_queue_out.put(ChangeNotification(
                        control_name=midi_control.info.mapped_to,
                        value=midi_control.value,
                        origin=MIDINotificationOrigin()
                    ))
                else:
                    #
                    # Pagination
                    page_changed = False
                    for pagination in self.midi_configuration.paginations.values():
                        if midi_control.value.value and midi_control.info == pagination.right:
                            self.context.current_page = min(self.context.current_page + 1, pagination.page_count - 1)
                            page_changed = True

                        elif midi_control.value.value and midi_control.info == pagination.left:
                            self.context.current_page = max(0, self.context.current_page - 1)
                            page_changed = True

                        if page_changed:
                            pass
                            # for page_midi_control in pagination.controls[self.context.current_page]:
                            #     message = page_midi_control.make_message(page_midi_control.info.device)
                            #     self.devices[page_midi_control.info.device.name].queue_out.put(message)
