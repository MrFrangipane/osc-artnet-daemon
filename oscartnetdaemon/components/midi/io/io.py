from oscartnetdaemon.components.midi.io.device import MIDIDevice
from oscartnetdaemon.components.midi.io.message import MIDIMessage
from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents


class MIDIIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting

        self.devices: dict[str, MIDIDevice] = dict()  # FIXME make a device repository ?
        # self.context: MIDIContext = None

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        """
        self.devices = dict()
        for device_info in self.components.configuration.device_infos.values():
            self.devices[device_info.name] = MIDIDevice(device_info, self.components.io_message_queue_in)
            self.devices[device_info.name].start()

    def send_message(self, message: MIDIMessage):
        self.devices[message.device_name].queue_out.put(message)

    def shutdown(self):
        """
        Gracefully shutdown all IO
        """
        for device in self.devices.values():
            device.stop()
