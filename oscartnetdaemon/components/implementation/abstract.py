import sys
from abc import ABC, abstractmethod
from multiprocessing import Queue

from oscartnetdaemon.components.domain.change_notification import ChangeNotification


class AbstractImplementation(ABC):

    def __init__(self):
        self.in_notifications: Queue[ChangeNotification] = None
        self.out_notifications: Queue[ChangeNotification] = None

    def exec_bootstrap(self, in_notifications_queue: Queue, out_notifications_queue: Queue):
        print(f"Bootstraping {self.__class__.__name__}")

        self.in_notifications = in_notifications_queue
        self.out_notifications = out_notifications_queue
        # TODO gracefully exit
        # https://stackoverflow.com/questions/26627382/python-multiprocessing-killing-a-process-gracefully ?
        try:
            self.exec()
        except KeyboardInterrupt:
            self.handle_termination()
            print(f"Terminated {self.__class__.__name__}")

    @abstractmethod
    def exec(self):
        """
        Implement this as a "run forever" loop
        Get and send notifications using self._in_notifications and self._out_notifications queues
        """
        pass

    @abstractmethod
    def handle_termination(self):
        pass
