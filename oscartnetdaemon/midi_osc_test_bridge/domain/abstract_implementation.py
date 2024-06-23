from abc import ABC, abstractmethod

from oscartnetdaemon.midi_osc_test_bridge.domain.change_notification import ChangeNotification


class AbstractImplementation(ABC):

    def __init__(self, domain):
        self.domain = domain

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def handle_change_notification(self, change_notification: ChangeNotification):
        pass
