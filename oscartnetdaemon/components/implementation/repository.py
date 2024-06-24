from typing import Type
from multiprocessing import Process, Queue

from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.implementation.pack import ImplementationPack
from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo


class ImplementationRepository:

    def __init__(self, configuration_info: ConfigurationInfo):
        self._configuration_info = configuration_info
        self._registered_types: list[Type[AbstractImplementation]] = list()
        self._implementation_packs: list[ImplementationPack] = list()

    def register_implementation_type(self, implementation_type: Type[AbstractImplementation]):
        if implementation_type not in self._registered_types:
            self._registered_types.append(implementation_type)
        else:
            raise ValueError(f"Implementation type {implementation_type.__name__} already registered")

        new_pack = ImplementationPack(
            implementation=implementation_type(self._configuration_info),
            notifications_queue_in=Queue(),
            notifications_queue_out=Queue()
        )
        self._implementation_packs.append(new_pack)

    def start_all(self):
        for pack in self._implementation_packs:
            pack.process = Process(
                target=pack.implementation.exec_bootstrap,
                args=(pack.notifications_queue_in, pack.notifications_queue_out)
            )
            pack.process.start()

    def terminate_all(self):
        for pack in self._implementation_packs:
            pack.process.kill()
            while pack.process.is_alive():
                pass
            print(f"{pack.implementation.__class__.__name__} exit code is {pack.process.exitcode}")

    def get_notifications(self) -> list[ChangeNotification]:
        notifications = []
        for pack in self._implementation_packs:
            while not pack.notifications_queue_out.empty():
                notification = pack.notifications_queue_out.get()
                notifications.append(notification)
        return notifications

    def put_notification(self, notification: ChangeNotification):
        for pack in self._implementation_packs:
            pack.notifications_queue_in.put(notification)
