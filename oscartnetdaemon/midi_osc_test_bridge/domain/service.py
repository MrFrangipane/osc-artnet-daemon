from oscartnetdaemon.midi_osc_test_bridge.osc.service import OSCService
from oscartnetdaemon.midi_osc_test_bridge.midi.service import MIDIService
from oscartnetdaemon.midi_osc_test_bridge.domain.controls import AbstractControl, FloatControl, ColorControl
from oscartnetdaemon.midi_osc_test_bridge.implementation.repository import ImplementationRepository


class Domain:

    def __init__(self):
        self.controls: dict[str, AbstractControl] = {
            'FaderA': FloatControl('Float'),
            'FaderB': ColorControl('Color')
        }

        self.implementations = ImplementationRepository()
        self.implementations.register_implementation_type(OSCService)
        self.implementations.register_implementation_type(MIDIService)

    def start(self):
        self.implementations.start_all()

        while True:
            for notification in self.implementations.get_notifications():
                self.controls[notification.control_name].value = notification.value
                self.implementations.put_notification(notification)

    def stop(self):
        self.implementations.terminate_all()
