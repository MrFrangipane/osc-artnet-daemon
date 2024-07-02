from oscartnetdaemon.domain_contract.variable.float import VariableFloat

from advanceddmxconsole.artnet.io.message import ArtnetIOMessage
from advanceddmxconsole.artnet.variable_info import ArtnetVariableInfo
from advanceddmxconsole.artnet.variable.scribble_mixin import ArtnetScribbleMixin


class ArtnetFader(VariableFloat, ArtnetScribbleMixin):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion

        if info.index == -1:
            return

        self.io_message_queue_out.put(ArtnetIOMessage(
            channel=info.index,
            value=int(self.value.value * 255)
        ))

        self.handle_scribble()

    def handle_io_message(self, message: ArtnetIOMessage):
        """
        From IO to ChangeNotification
        """
        pass
