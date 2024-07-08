import logging

from copy import copy
from multiprocessing import Event, Process, Queue

from mido.messages import Message
from mido.parser import Parser

from oscartnetdaemon.components.midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.qusb.constants import QuSbConstants
from oscartnetdaemon.components.qusb.io.fast_socket import FastSocket
from oscartnetdaemon.components.qusb.io.message import QuSbIOMessage
from oscartnetdaemon.components.qusb.parameter_type_enum import QuSbParameterType


_logger = logging.getLogger("QuSbDevice")


def process_midi_message(midi_message: Message, io_message: QuSbIOMessage):
    if midi_message is None or midi_message.type == MIDIMessageType.ActiveSensing.value:
        return

    if midi_message.type == MIDIMessageType.SysEx.value:
        # TODO: VU meters here ?
        return

    if midi_message.type == MIDIMessageType.ControlChange.value:

        if midi_message.control == QuSbConstants.NRPN_CHANNEL:
            io_message.channel = midi_message.value

        elif midi_message.control == QuSbConstants.NRPN_PARAMETER:
            io_message.parameter = QuSbConstants.CHANNEL_PARAMETER_CODE_TO_ENUM.get(
                midi_message.value,
                QuSbParameterType.Unknown
            )

        elif midi_message.control == QuSbConstants.NRPN_VALUE:
            io_message.value = midi_message.value

        elif midi_message.control == QuSbConstants.NRPN_DATA_ENTRY_FINE:
            if io_message.parameter != QuSbParameterType.Unknown:
                # TODO check if all values are set before ?
                io_message.is_complete = True


def process_io_message(socket_queue_out: "Queue[bytes]", io_message: QuSbIOMessage):
    if io_message.parameter == QuSbParameterType.Unknown:
        return

    socket_queue_out.put(Message(
        type=MIDIMessageType.ControlChange.value,
        control=QuSbConstants.NRPN_CHANNEL,
        value=io_message.channel
    ).bin())
    socket_queue_out.put(Message(
        type=MIDIMessageType.ControlChange.value,
        control=QuSbConstants.NRPN_PARAMETER,
        value=QuSbConstants.CHANNEL_ENUM_PARAMETER_CODE[io_message.parameter],
    ).bin())
    socket_queue_out.put(Message(
        type=MIDIMessageType.ControlChange.value,
        control=QuSbConstants.NRPN_VALUE,
        value=io_message.value,
    ).bin())
    socket_queue_out.put(Message(
        type=MIDIMessageType.ControlChange.value,
        control=QuSbConstants.NRPN_DATA_ENTRY_FINE,
        value=0,  # TODO: check if really always 0
    ).bin())


def _loop(host: str, port: int, should_stop: Event, io_queue_out: "Queue[QuSbIOMessage]", io_queue_in: "Queue[QuSbIOMessage]"):
    fast_socket = FastSocket(host, port)
    fast_socket.start()
    parser = Parser()

    io_message: QuSbIOMessage = QuSbIOMessage()

    #
    # Request device state
    midi_message_request = Message(
        type=MIDIMessageType.SysEx.value,
        data=QuSbConstants.SYSEX_REQUEST_STATE
    )
    fast_socket.queue_out.put(midi_message_request.bin())
    try:
        while not should_stop.is_set():
            while not fast_socket.queue_in.empty():
                parser.feed(fast_socket.queue_in.get())

            while parser.messages:
                midi_message = parser.messages.popleft()

                process_midi_message(midi_message, io_message)
                if io_message.is_complete:
                    io_queue_in.put(copy(io_message))
                    io_message = QuSbIOMessage()

            while not io_queue_out.empty():
                process_io_message(fast_socket.queue_out, io_queue_out.get())

    except KeyboardInterrupt:
        pass

    finally:
        fast_socket.stop()


class QuSbDevice:
    """
    Send/receive MIDI messages over TCP from Allen&Heath Qu-SB
    Converts to/from QuSbIOMessage
    """

    def __init__(self, host: str, port: int, queue_in: "Queue[QuSbIOMessage]", should_stop: Event):
        self.host = host
        self.port = port

        self.queue_in = queue_in
        self.queue_out: "Queue[QuSbIOMessage]" = Queue()

        self.should_stop = should_stop

        self.process: Process | None = None

    def start(self):
        self.process = Process(target=_loop, args=[
            self.host, self.port, self.should_stop, self.queue_out, self.queue_in
        ])
        self.process.start()

    def is_alive(self) -> bool:
        return self.process.is_alive()
