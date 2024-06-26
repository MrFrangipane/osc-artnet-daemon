from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


class AAFloat(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        print(self.__class__.__name__, notification)

    def handle_implementation_message(self, message: AbstractIOMessage):
        print(self.__class__.__name__, message)

