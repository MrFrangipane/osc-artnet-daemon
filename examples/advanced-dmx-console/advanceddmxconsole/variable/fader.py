from oscartnetdaemon.domain_contract.variable.float import VariableFloat

from advanceddmxconsole.advanced_dmx_console import AdvancedDmxConsole
from advanceddmxconsole.io.message import ArtnetIOMessage
from advanceddmxconsole.variable.scribble_mixin import ArtnetScribbleMixin


class ArtnetFader(VariableFloat, ArtnetScribbleMixin):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        AdvancedDmxConsole().handle_fader(self.info, self.value)
        self.handle_scribble()

    def handle_io_message(self, message: ArtnetIOMessage):
        """
        From IO to ChangeNotification
        """
        pass
