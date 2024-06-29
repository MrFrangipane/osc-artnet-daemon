from oscartnetdaemon.components.new_osc.io.message import OSCMessage
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat
from oscartnetdaemon.components.new_osc.variable_info import OSCVariableInfo


class OSCRecallSlot(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        pass

    def handle_io_message(self, message: OSCMessage):
        """
        From IO to ChangeNotification
        """
        pass
