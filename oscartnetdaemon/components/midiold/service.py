from multiprocessing import Queue
from threading import Thread

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.domain.entities.control_update_origin_enum import DomainControlUpdateOrigin
from oscartnetdaemon.components.midi.abstract_service import AbstractMIDIService
from oscartnetdaemon.components.midi.control_repository import MIDIControlRepository
from oscartnetdaemon.components.midi.device import MIDIDevice
from oscartnetdaemon.components.midi.entities.context import MIDIContext
from oscartnetdaemon.components.midi.entities.control_update_info import MIDIControlUpdateInfo
from oscartnetdaemon.components.midi.entities.message import MIDIMessage
from oscartnetdaemon.components.midi.message_handler import MIDIMessageHandler


class MIDIService(AbstractMIDIService):

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.control_repository: MIDIControlRepository = None
        self.message_handler: MIDIMessageHandler = None
        self.queue_in: Queue[MIDIMessage] = Queue()
        self.queues_out: dict[str, Queue[MIDIMessage]] = dict()
        self._thread: Thread = None
        self.context: MIDIContext = None

    def start(self):
        self.control_repository = MIDIControlRepository()
        self.control_repository.create_controls(Components().midi_configuration.controls.values())

        self.devices = dict()  # FIXME make a device repository
        for device_info in Components().midi_configuration.devices.values():
            self.devices[device_info.name] = MIDIDevice(device_info, self.queue_in)
            self.devices[device_info.name].components_singleton = Components
            self.devices[device_info.name].start()

        self.message_handler = MIDIMessageHandler(
            control_repository=self.control_repository
        )

        self.context = MIDIContext(
            current_page=0,
            current_layer=list(list(Components().midi_configuration.layer_groups.values())[0].layers.values())[0]
        )

        self.is_running = True
        self._thread = Thread(target=self.loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.is_running = False
        for device in self.devices.values():
            device.stop()

    def loop(self):
        while self.is_running:
            message = self.queue_in.get()
            self.message_handler.handle(message, self.context)

    def notify_update(self, update_info: MIDIControlUpdateInfo):
        #
        # TODO : page and layer changes
        #
        if update_info.mapped_to:
            Components().domain_service.notify_update(
                origin=DomainControlUpdateOrigin.MIDI,
                control_name=update_info.mapped_to,
                value=update_info.value
            )
