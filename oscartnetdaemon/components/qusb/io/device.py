import logging

from copy import copy
from multiprocessing import Event, Process, Queue

from mido.messages import Message
from mido.sockets import BaseIOPort, connect

from oscartnetdaemon.components.midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.qusb.constants import QuSbConstants
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


def process_io_message(midi_tcp: BaseIOPort, io_message: QuSbIOMessage):
    if io_message.parameter == QuSbParameterType.Unknown:
        return

    midi_tcp.send(Message(
        type=MIDIMessageType.ControlChange.value,
        control=QuSbConstants.NRPN_CHANNEL,
        value=io_message.channel
    ))
    midi_tcp.send(Message(
        type=MIDIMessageType.ControlChange.value,
        control=QuSbConstants.NRPN_PARAMETER,
        value=QuSbConstants.CHANNEL_ENUM_PARAMETER_CODE[io_message.parameter],
    ))
    midi_tcp.send(Message(
        type=MIDIMessageType.ControlChange.value,
        control=QuSbConstants.NRPN_VALUE,
        value=io_message.value,
    ))
    midi_tcp.send(Message(
        type=MIDIMessageType.ControlChange.value,
        control=QuSbConstants.NRPN_DATA_ENTRY_FINE,
        value=0,  # TODO: check if really always 0
    ))


def _loop(host: str, port: int, should_stop: Event, queue_out: "Queue[QuSbIOMessage]", queue_in: "Queue[QuSbIOMessage]"):
    midi_tcp: BaseIOPort = connect(host, port)
    io_message: QuSbIOMessage = QuSbIOMessage()

    #
    # Request device state
    midi_message_request = Message(
        type=MIDIMessageType.SysEx.value,
        data=QuSbConstants.SYSEX_REQUEST_STATE
    )
    midi_tcp.send(midi_message_request)
    while True:
        midi_message = midi_tcp.receive()
        if bytearray(midi_message.bytes()[1:-1]) == QuSbConstants.SYSEX_REQUEST_STATE_END:
            break

        process_midi_message(midi_message, io_message)
        if io_message.is_complete:
            queue_in.put(copy(io_message))
            io_message = QuSbIOMessage()

    #
    # Actual loop
    try:
        while not should_stop.is_set():
            midi_message = midi_tcp.receive(block=False)

            if midi_message is None:
                continue

            process_midi_message(midi_message, io_message)
            if io_message.is_complete:
                print(io_message)
                queue_in.put(copy(io_message))
                io_message = QuSbIOMessage()
                print(io_message)

            while not queue_out.empty():
                process_io_message(midi_tcp, queue_out.get())

    except KeyboardInterrupt:
        pass

    finally:
        midi_tcp.close()


class QuSbDevice:

    def __init__(self, host: str, port: int, queue_in: "Queue[QuSbIOMessage]", should_stop: Event):
        self.host = host
        self.port = port

        self.queue_in = queue_in
        self.queue_out: "Queue[QuSbIOMessage]" = Queue()

        self.should_stop = should_stop

        self.midi_tcp: BaseIOPort | None = None
        self.io_message: QuSbIOMessage = QuSbIOMessage()

        self.process: Process | None = None

    def start(self):
        self.process = Process(target=_loop, args=[
            self.host, self.port, self.should_stop, self.queue_out, self.queue_in
        ])
        self.process.start()

    def is_alive(self) -> bool:
        return self.process.is_alive()
