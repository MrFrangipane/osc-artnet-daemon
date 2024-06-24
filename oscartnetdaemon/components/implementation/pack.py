from dataclasses import dataclass
from multiprocessing import Process, Queue

from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation


@dataclass
class ImplementationPack:
    implementation: AbstractImplementation
    in_queue: "Queue[ChangeNotification]"
    out_queue: "Queue[ChangeNotification]"
    process: Process | None = None
