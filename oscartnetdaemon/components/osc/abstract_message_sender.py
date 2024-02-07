from abc import ABC, abstractmethod

from oscartnetdaemon.core.osc_client_info import OSCClientInfo


class AbstractOSCMessageSender(ABC):

    @abstractmethod
    def register_client(self, info: OSCClientInfo):
        pass

    @abstractmethod
    def unregister_client(self, info: OSCClientInfo):
        pass

    @abstractmethod
    def send(self, control_name, value, sender):
        pass

    @abstractmethod
    def notify_punch(self, sender, is_punch):
        pass

    @abstractmethod
    def send_mood_to_all(self):
        pass
