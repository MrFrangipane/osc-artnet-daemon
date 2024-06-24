from dataclasses import dataclass
from multiprocessing import Process, Queue

from oscartnetdaemon.midi_osc_test_bridge.domain.change_notification import ChangeNotification
from oscartnetdaemon.midi_osc_test_bridge.implementation.abstract import AbstractImplementation


@dataclass
class ImplementationPack:
    implementation: AbstractImplementation
    in_queue: Queue
    out_queue: Queue
    process: Process | None = None
