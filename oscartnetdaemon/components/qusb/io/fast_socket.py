import socket
import time

from multiprocessing import Event, Process, Queue


def socket_loop(host: str, port: int, queue_in: "Queue[bytes]", queue_out: "Queue[bytes]", should_stop: Event):
    midi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    midi_socket.settimeout(0.0001)
    midi_socket.connect((host, port))

    try:
        while not should_stop.is_set():
            try:
                queue_in.put(midi_socket.recv(2048))
            except TimeoutError:
                pass

            while not queue_out.empty():
                midi_socket.send(queue_out.get())

    except KeyboardInterrupt:
        midi_socket.close()


class FastSocket:
    def __init__(self, host: str, port: int):
        self.queue_in = Queue()
        self.queue_out = Queue()
        self.should_stop = Event()

        self.process = Process(target=socket_loop, args=(
            host, port,
            self.queue_in, self.queue_out,
            self.should_stop
        ))

    def start(self):
        self.process.start()

    def stop(self):
        self.should_stop.set()
        while self.process.is_alive():
            time.sleep(0.01)
