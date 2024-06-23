from dataclasses import dataclass
from typing import Type

from oscartnetdaemon.midi_osc_test_bridge.osc.service import OSCService
from oscartnetdaemon.midi_osc_test_bridge.midi.service import MIDIService
from oscartnetdaemon.midi_osc_test_bridge.domain.change_notification import ChangeNotification
from oscartnetdaemon.midi_osc_test_bridge.domain.abstract_implementation import AbstractImplementation
from oscartnetdaemon.midi_osc_test_bridge.domain.controls import AbstractControl, FloatControl, ColorControl


class Domain:

    def __init__(self):
        self.controls: dict[str, AbstractControl] = {
            'FaderA': FloatControl('Float'),
            'FaderB': ColorControl('Color')
        }

        # TODO use singleton and not self
        self.implementations: list[AbstractImplementation] = [
            OSCService(domain=self),
            MIDIService(domain=self)
        ]

    def add_implementation(self, implementation_type: Type[AbstractImplementation]):
        self.implementations.append(implementation_type(domain=self))

    def start(self):
        for implementation in self.implementations:
            implementation.start()

    def notify_change(self, change_notification: ChangeNotification):
        self.controls[change_notification.control_name].value = change_notification.value
        for implementation in self.implementations:
            implementation.handle_change_notification(change_notification)
