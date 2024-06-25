from multiprocessing import Queue

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.midi.configuration_loader import load_midi_configuration
from oscartnetdaemon.components.midi.control_repository import MIDIControlRepository
from oscartnetdaemon.components.midi.controls.abstract import MIDIAbstractControl
from oscartnetdaemon.components.midi.device import MIDIDevice
from oscartnetdaemon.components.midi.entities.context import MIDIContext
from oscartnetdaemon.components.midi.entities.control_role_enum import MIDIControlRole
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

        self.activate_first_page_first_layer()
        self.send_all_messages()

    def activate_first_page_first_layer(self):
        # FIXME: don't assume there's only one pagination and one layer group
        first_layer = list(list(self.midi_configuration.layer_groups.values())[0].layers.values())[0]
        self.context = MIDIContext(
            current_page=0,
            current_layer=first_layer
        )
        trigger = self.control_repository.controls[first_layer.trigger.name]
        trigger.value.value = 1.0
        # self.post_message_for_control(trigger)

    def send_all_messages(self):
        for control in self.control_repository.controls.values():
            self.post_message_for_control(control)

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
                self.post_message_for_control(midi_control)

    def handle_termination(self):
        for device in self.devices.values():
            device.stop()

    def handle_message(self, message: MIDIMessage):
        # FIXME: use classes to deal with pages and layers (and get rid of all the nested info)
        handled = False
        for midi_control in self.control_repository.controls.values():

            if midi_control.info.role == MIDIControlRole.Mapped:
                if midi_control.complies_with(message, self.context) and midi_control.handle_message(message, self.context):
                    handled = True
                    self.notifications_queue_out.put(ChangeNotification(
                        control_name=midi_control.info.mapped_to,
                        value=midi_control.value,
                        origin=MIDINotificationOrigin()
                    ))

            elif midi_control.info.role == MIDIControlRole.PageSelector:
                if midi_control.complies_with(message, self.context) and midi_control.handle_message(message, self.context):
                    # FIXME: this is terrible and should be dealt with with classes
                    self.post_message_for_control(midi_control)
                    handled = True
                    page_changed = False
                    for pagination in self.midi_configuration.paginations.values():
                        if midi_control.value.value and midi_control.info == pagination.right:
                            self.context.current_page = min(self.context.current_page + 1, pagination.page_count - 1)
                            page_changed = True

                        elif midi_control.value.value and midi_control.info == pagination.left:
                            self.context.current_page = max(0, self.context.current_page - 1)
                            page_changed = True

                        if page_changed:
                            for page_midi_control_info in pagination.controls[self.context.current_page].values():
                                page_midi_control = self.control_repository.controls[page_midi_control_info.name]
                                self.post_message_for_control(page_midi_control)

            elif midi_control.info.role == MIDIControlRole.LayerTrigger:
                if midi_control.complies_with(message, self.context) and midi_control.handle_message(message, self.context):
                    # FIXME: this is terrible and should be dealt with with classes
                    handled = True
                    layer_changed = False
                    for layer_group in self.midi_configuration.layer_groups.values():
                        for layer in layer_group.layers.values():
                            if not midi_control.value.value:
                                continue

                            if layer != self.context.current_layer and midi_control.info == layer.trigger:
                                self.context.current_layer = layer
                                layer_changed = True
                                break

                        if layer_changed:
                            for layer in layer_group.layers.values():
                                trigger = self.control_repository.controls[layer.trigger.name]
                                trigger.value.value = float(layer == self.context.current_layer)
                                self.post_message_for_control(trigger)

                            for layer_midi_control_info in self.context.current_layer.controls:
                                layer_midi_control = self.control_repository.controls[layer_midi_control_info.name]
                                self.post_message_for_control(layer_midi_control)

            elif midi_control.info.role == MIDIControlRole.Unused:
                if midi_control.complies_with(message, self.context) and midi_control.handle_message(message, self.context):
                    # FIXME: why is this never called ?
                    handled = True

        if not handled:
            print(message)

    def post_message_for_control(self, midi_control: MIDIAbstractControl):
        page_ok = midi_control.info.page == -1 or midi_control.info.page == self.context.current_page
        layer_ok = midi_control.info.layer_name == "" or midi_control.info.layer_name == self.context.current_layer.name
        if not page_ok or not layer_ok:
            return

        self.devices[midi_control.info.device.name].queue_out.put(midi_control.make_message())
