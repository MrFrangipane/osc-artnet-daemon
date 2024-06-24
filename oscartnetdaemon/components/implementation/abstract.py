from abc import ABC, abstractmethod
from multiprocessing import Queue

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.domain.change_notification import ChangeNotification


class AbstractImplementation(ABC):

    def __init__(self, configuration_info: ConfigurationInfo):
        self.configuration_info = configuration_info
        self.notification_queue_in: Queue[ChangeNotification] = None
        self.notifications_queue_out: Queue[ChangeNotification] = None

    def exec_bootstrap(self, notification_queue_in: Queue, notifications_queue_out: Queue):
        print(f"Bootstraping {self.__class__.__name__}")

        self.notification_queue_in = notification_queue_in
        self.notifications_queue_out = notifications_queue_out
        try:
            self.exec()
            pass
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
