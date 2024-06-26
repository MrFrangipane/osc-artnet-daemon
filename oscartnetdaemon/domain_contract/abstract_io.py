from abc import ABC, abstractmethod
from multiprocessing import Queue

from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage


class AbstractIO(ABC):

    def __init__(self, io_message_queue_in: "Queue[AbstractIOMessage]", io_message_queue_out: "Queue[AbstractIOMessage]"):
        self.io_message_queue_in = io_message_queue_in
        self.io_message_queue_out = io_message_queue_out

    @abstractmethod
    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Gracefully shutdown all IO
        """
        pass
