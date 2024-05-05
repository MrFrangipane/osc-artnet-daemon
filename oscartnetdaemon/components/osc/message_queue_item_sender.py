import colorsys
from queue import Queue

from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.components.osc.message_queue_item import OSCMessageQueueItem


class OSCMessageQueueItemSender:
    def __init__(self, message_queue: Queue):
        self.message_queue: Queue[OSCMessageQueueItem] = message_queue
        self.clients: dict[str, SimpleUDPClient] = dict()
        self._is_running = False

    def start(self):
        self._is_running = True
        while self._is_running:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                if message.client_ip not in self.clients:
                    self.clients[message.client_ip] = SimpleUDPClient(message.client_ip, message.client_port)

                for client in list(self.clients.values()):
                    # fixme: create classes for each widget, and move to message handler ?
                    if message.type == 'fader':
                        client.send_message(message.address + '/fader', message.value)
                        client.send_message(message.address + '/value', int(message.value * 255))
                        # client.send_message(message.address + '/name', "A fader")

                    elif message.type == 'palette_select':
                        client.send_message(message.address + '/radio', message.value)

                    elif message.type == 'color_wheel':
                        client.send_message(message.address + '/encoder', message.value)
                        r, g, b = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(message.value, 1.0, 1.0))
                        client.send_message(message.address + '/color', f"{r:02x}{g:02x}{b:02x}")

                    elif message.type == 'recall_slot':
                        client.send_message(message.address, message.value)
