from abc import ABC, abstractmethod


class AbstractOSCServer(ABC):

    def __init__(self, address, port):
        self.address = address
        self.port = port

        self._last_message_datetime = None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def _handle(self, address, *values):
        pass
