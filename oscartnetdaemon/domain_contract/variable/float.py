from abc import ABC
from multiprocessing import Queue

from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.value.float import ValueFloat
from oscartnetdaemon.domain_contract.variable.abstract import AbstractVariable
from oscartnetdaemon.domain_contract.variable_info import VariableInfo


class VariableFloat(AbstractVariable, ABC):

    def __init__(self, info: VariableInfo, io_message_queue_out: "Queue[AbstractIOMessage]", notification_queue_out: "Queue[ChangeNotification]"):
        super().__init__(info, io_message_queue_out, notification_queue_out)
        self.value = ValueFloat()
