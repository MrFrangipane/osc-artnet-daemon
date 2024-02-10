from abc import ABC, abstractmethod

from oscartnetdaemon.core.show.show import Show


class AbstractShowStore(ABC):
    def __init__(self):
        self.show: Show = None

    @abstractmethod
    def load_show(self):
        pass
