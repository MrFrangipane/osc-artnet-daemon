from oscartnetdaemon.domain_contract.variable.float import VariableFloat
from oscartnetdaemon.components.qusb.io.message import QuSbIOMessage
from oscartnetdaemon.components.qusb.variable_info import QuSbVariableInfo


class QuSbFader(VariableFloat):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        info: QuSbVariableInfo = self.info  # FIXME type hint for autocompletion

        # Do stuff here

    def handle_io_message(self, message: QuSbIOMessage):
        """
        From IO to ChangeNotification
        """
        info: QuSbVariableInfo = self.info  # FIXME type hint for autocompletion

        # Do stuff, update value here

        self.notify_change()
