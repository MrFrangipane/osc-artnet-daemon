import time
from multiprocessing import Event, Process, Queue

import mido

from oscartnetdaemon.components.midi.io.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.io.message import MIDIMessage
from oscartnetdaemon.components.midi.io.message_type_enum import MIDIMessageType


def receive(queue_in: "Queue[MIDIMessage]", device_info: MIDIDeviceInfo, should_exit: Event):
    midi_in = mido.open_input(device_info.in_port_name)
    try:
        while not should_exit.is_set():
            mido_message = midi_in.receive(timeout=0.2)  # don't block, we want the KeyboardInterrupt to work
            if mido_message is None:
                continue
            mido_message_vars = vars(mido_message)
            mido_message_vars['device_name'] = device_info.name
            try:
                message = MIDIMessage.from_dict(mido_message_vars)
                queue_in.put(message)
            except ValueError:
                print(f'Midi device cant deal with <{mido_message}>')

    except KeyboardInterrupt:
        pass

    except Exception as e:
        raise

    finally:
        midi_in.close()


def send(queue_out: "Queue[MIDIMessage]", device_info: MIDIDeviceInfo, should_exit: Event):
    midi_out = mido.open_output(device_info.out_port_name)
    try:
        while not should_exit.is_set():
            while not queue_out.empty():
                message = queue_out.get()
                if message.type == MIDIMessageType.PitchWheel:
                    midi_out.send(mido.Message(
                        type=message.type.value,
                        channel=message.channel,
                        pitch=message.pitch
                    ))

                elif message.type == MIDIMessageType.NoteOn:
                    midi_out.send(mido.Message(
                        type=message.type.value,
                        channel=message.channel,
                        note=message.note,
                        velocity=message.velocity
                    ))

                elif message.type == MIDIMessageType.SysEx:
                    midi_out.send(mido.Message(
                        type=message.type.value,
                        data=message.data
                    ))

                else:
                    print(f'Midi device cant send <{message}>')

    except KeyboardInterrupt:
        pass

    except Exception as e:
        raise

    finally:
        midi_out.close()


class MIDIDevice:
    def __init__(self, info: MIDIDeviceInfo, queue_in: Queue):
        self.info = info
        self.queue_in: Queue[MIDIMessage] = queue_in
        self.queue_out: Queue[MIDIMessage] = Queue()
        self.process_should_exit = Event()
        self.process_in: Process = None
        self.process_out: Process = None

    def start(self):
        self.process_in = Process(target=receive, args=(self.queue_in, self.info, self.process_should_exit))
        self.process_out = Process(target=send, args=(self.queue_out, self.info, self.process_should_exit))

        self.process_in.start()
        self.process_out.start()

    def stop(self):
        self.process_should_exit.set()
        while self.process_in.is_alive() or self.process_out.is_alive():
            time.sleep(0.01)
