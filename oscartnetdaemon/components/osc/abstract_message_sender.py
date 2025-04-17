from abc import ABC, abstractmethod

from oscartnetdaemon.core.osc_client_info import OSCClientInfo


class AbstractOSCMessageSender(ABC):

    @abstractmethod
    def ensure_registered(self, ip_address: str, port: int):
        pass

    @abstractmethod
    def register_client(self, info: OSCClientInfo):
        pass

    @abstractmethod
    def unregister_client(self, info: OSCClientInfo):
        pass

    @abstractmethod
    def send(self, control_name, value, sender_ip):
        pass

    @abstractmethod
    def notify_punch(self, sender, is_punch):
        pass

    @abstractmethod
    def send_mood_to_all(self):
        pass

    @abstractmethod
    def send_pattern_names_to_all(self):
        pass

    @abstractmethod
    def send_to_all_raw(self, address, value):
        pass
