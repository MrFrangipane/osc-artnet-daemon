from dataclasses import dataclass


from oscartnetdaemon.midi_osc_test_bridge.osc.service import OSCService
from oscartnetdaemon.midi_osc_test_bridge.midi.service import MIDIService
from oscartnetdaemon.midi_osc_test_bridge.domain.change_notification import ChangeNotification


@dataclass
class DomainControl:
    name: str
    value: float = 0.0


class Domain:

    def __init__(self):
        self.controls: dict[str, DomainControl] = {
            'FaderA': DomainControl('FaderA'),
            'FaderB': DomainControl('FaderB')
        }

        # TODO use singleton and not self
        self.osc = OSCService(domain=self)
        self.midi = MIDIService(domain=self)

    def start(self):
        self.osc.start()
        self.midi.start()

    def notify_change(self, change_notification: ChangeNotification):
        self.controls[change_notification.control_name].value = change_notification.value
        self.osc.handle_change_notification(change_notification)
        self.midi.handle_change_notification(change_notification)
