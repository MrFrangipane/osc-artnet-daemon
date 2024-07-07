from oscartnetdaemon.domain_contract.variable.float import VariableFloat

from advanceddmxconsole.io.message import ArtnetIOMessage


class ArtnetIndicator(VariableFloat):
    """
    Dummy so we can generate notifications
    FIXME: is this really needed ?
    """

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        pass

    def handle_io_message(self, message: ArtnetIOMessage):
        """
        From IO to ChangeNotification
        """
        pass
