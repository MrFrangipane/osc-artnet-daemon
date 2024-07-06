from multiprocessing import Queue

from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable_repository import VariableRepository


class ArtnetVariableRepository(VariableRepository):

    def initialize(self):
        pass

    def create_variables(self, configuration: BaseConfiguration, io_message_queue_out: "Queue[AbstractIOMessage]"):
        pass

    def handle_change_notification(self, notification: ChangeNotification):
        """
        Calls associated Variable's handle_change_notification()
        Updates Variable's value beforehand if pertinent
        """
        pass

    def broadcast_io_message(self, message: AbstractIOMessage):
        """
        Asks all variables to handle the message
        """
        pass

    def notify_all_variables(self):
        """
        Send a notification to all variables
        Useful when app starts or when new client connects
        """
        pass
