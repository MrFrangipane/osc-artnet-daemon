from queue import Queue
from oscartnetdaemon.components.osc.message_queue_item import OSCMessageQueueItem


class OSCMessageHandler:

    def __init__(self, message_queue: Queue[OSCMessageQueueItem]):
        self.message_queue = message_queue

    def handle_fader(self, client_address, osc_address, osc_value):
        self.message_queue.put(OSCMessageQueueItem(
            client_ip=client_address[0],
            client_port=client_address[1],
            type="fader",
            address='/'.join(osc_address.split('/')[:-1]),
            value=osc_value
        ))

    def handle_palette_select(self, client_address, osc_address, osc_value):
        self.message_queue.put(OSCMessageQueueItem(
            client_ip=client_address[0],
            client_port=client_address[1],
            type="palette_select",
            address='/'.join(osc_address.split('/')[:-1]),
            value=osc_value
        ))

    def handle_color_wheel(self, client_address, osc_address, osc_value):
        self.message_queue.put(OSCMessageQueueItem(
            client_ip=client_address[0],
            client_port=client_address[1],
            type="color_wheel",
            address='/'.join(osc_address.split('/')[:-1]),
            value=osc_value
        ))

    def handle_recall_slot(self, client_address, osc_address, osc_value):
        self.message_queue.put(OSCMessageQueueItem(
            client_ip=client_address[0],
            client_port=client_address[1],
            type="recall_slot",
            address=osc_address,
            value=osc_value
        ))

    @staticmethod
    def handle_default(client_address, osc_address, osc_value):
        print("DEFAULT", client_address, osc_address, osc_value)
