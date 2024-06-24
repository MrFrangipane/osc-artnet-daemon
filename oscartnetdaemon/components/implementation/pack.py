from dataclasses import dataclass
from multiprocessing import Process, Queue

from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation


@dataclass
class ImplementationPack:
    implementation: AbstractImplementation
    notifications_queue_in: "Queue[ChangeNotification]"
    notifications_queue_out: "Queue[ChangeNotification]"
    process: Process | None = None
