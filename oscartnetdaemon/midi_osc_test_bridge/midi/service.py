from oscartnetdaemon.midi_osc_test_bridge.domain.abstract_implementation import AbstractImplementation
from oscartnetdaemon.midi_osc_test_bridge.domain.change_notification import ChangeNotification


class MIDIService(AbstractImplementation):

    def start(self):
        pass

    def handle_change_notification(self, change_notification: ChangeNotification):
        pass
