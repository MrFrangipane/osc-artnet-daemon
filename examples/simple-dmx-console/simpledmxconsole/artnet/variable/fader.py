from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.value.text import ValueText
from oscartnetdaemon.domain_contract.variable.float import VariableFloat

from simpledmxconsole.artnet.io.message import ArtnetIOMessage
from simpledmxconsole.artnet.variable_info import ArtnetVariableInfo


class ArtnetFader(VariableFloat):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion

        if info.dmx_channel == -1:
            return

        self.io_message_queue_out.put(ArtnetIOMessage(
            channel=info.dmx_channel,
            value=int(self.value.value * 255)
        ))

        self.handle_scribble()

    def handle_io_message(self, message: ArtnetIOMessage):
        """
        From IO to ChangeNotification
        """
        pass

    def handle_scribble(self):
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion

        if info.scribble_caption:
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.scribble_caption,
                new_value=ValueText(info.caption)
            ))

        if info.scribble_value:
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.scribble_value,
                new_value=ValueText(str(int(self.value.value * 255)))
            ))
