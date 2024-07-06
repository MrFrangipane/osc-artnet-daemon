from oscartnetdaemon.domain_contract.variable.float import VariableFloat

from advanceddmxconsole.io.message import ArtnetIOMessage
from advanceddmxconsole.variable_info import ArtnetVariableInfo
from advanceddmxconsole.variable.scribble_mixin import ArtnetScribbleMixin
from advanceddmxconsole.rename_me import RenameMe


class ArtnetFader(VariableFloat, ArtnetScribbleMixin):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        RenameMe().handle_fader(self.info, self.value)
        self.handle_scribble()

    def handle_io_message(self, message: ArtnetIOMessage):
        """
        From IO to ChangeNotification
        """
        pass
