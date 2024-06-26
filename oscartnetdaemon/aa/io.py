from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from multiprocessing import Queue

from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage


class AAIO(AbstractIO):

    def __init__(self, io_message_queue_in: "Queue[AbstractIOMessage]", io_message_queue_out: "Queue[AbstractIOMessage]"):
        super().__init__(io_message_queue_in, io_message_queue_out)

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        """
        pass

    def shutdown(self):
        """
        Gracefully shutdown all IO
        """
        pass
