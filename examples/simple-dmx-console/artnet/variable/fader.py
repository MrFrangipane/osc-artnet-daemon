from artnet.io.message import ArtnetIOMessage
from artnet.variable_info import ArtnetVariableInfo
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat
from oscartnetdaemon.domain_contract.value.text import ValueText


class ArtnetFader(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion

        if info.dmx_channel == -1:
            return

        int_value = int(self.value.value * 255)
        self.io_message_queue_out.put(ArtnetIOMessage(
            channel=info.dmx_channel,
            value=int_value
        ))
        # TODO
        # self.notification_queue_out.put(ChangeNotification(
        #     info=ScribbleRepository().top[info.dmx_channel],
        #     value=ValueText(f"{int_value}")
        # ))

    def handle_io_message(self, message: ArtnetIOMessage):
        """
        From IO to ChangeNotification
        """
        pass
