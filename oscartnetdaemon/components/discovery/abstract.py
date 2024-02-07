from abc import ABC, abstractmethod


class AbstractDiscovery(ABC):
    def __init__(self, address_mask: str):
        self._address_mask = address_mask

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
