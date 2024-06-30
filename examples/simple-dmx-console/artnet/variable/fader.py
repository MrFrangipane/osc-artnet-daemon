from artnet.io.message import ArtnetMessage
from artnet.variable_info import ArtnetVariableInfo
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


class ArtnetFader(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion

        # Do stuff here

    def handle_io_message(self, message: ArtnetMessage):
        """
        From IO to ChangeNotification
        """
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion

        # Do stuff, update value here

        self.notify_change()
