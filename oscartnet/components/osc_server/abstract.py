from abc import ABC, abstractmethod


class AbstractOSCServer(ABC):

    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = 8000

    def __init__(self):
        self.host = self.DEFAULT_HOST
        self.port = self.DEFAULT_PORT

        self.last_message_datetime = None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def _handle(self, address, *values):
        pass
