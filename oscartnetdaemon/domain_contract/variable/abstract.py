from abc import ABC, abstractmethod
from multiprocessing import Queue

from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.value.base import BaseValue
from oscartnetdaemon.domain_contract.variable_info import VariableInfo


class AbstractVariable(ABC):

    def __init__(self, info: VariableInfo, io_message_queue_out: "Queue[AbstractIOMessage]", notification_queue_out: "Queue[ChangeNotification]"):
        self.info = info
        self.value: BaseValue | None = None
        self.io_message_queue_out = io_message_queue_out
        self.notification_queue_out = notification_queue_out

    @abstractmethod
    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        pass

    @abstractmethod
    def handle_io_message(self, message: AbstractIOMessage):
        """
        From IO to ChangeNotification
        """
        pass
