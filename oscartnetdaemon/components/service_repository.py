import time
from multiprocessing import Process
from typing import Type

from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.change_notification_scope_enum import ChangeNotificationScope
from oscartnetdaemon.domain_contract.service import Service
from oscartnetdaemon.domain_contract.service_bundle import ServiceBundle
from oscartnetdaemon.python_extensions.queue import clear


class ServiceRepository:

    def __init__(self):
        self.service_bundles: dict[str, ServiceBundle] = dict()
        self.verbose = False

    def register(self, registerer: Type[AbstractServiceRegisterer]):
        registration_info = registerer.make_registration_info()
        new_bundle = ServiceBundle(service=Service(registration_info))
        self.service_bundles[registration_info.io_type.__name__] = new_bundle

    def exec(self):
        for bundle in self.service_bundles.values():
            bundle.process = Process(target=bundle.service.exec)
            bundle.process.start()

            print(f"Starting service '{bundle.service.io_type.__name__}'...")
            while not bundle.service.startup_done.is_set() and bundle.process.is_alive():
                time.sleep(.1)

            if not bundle.process.is_alive():
                print(f"Service '{bundle.service.io_type.__name__}' finished with code {bundle.process.exitcode}")

        print("Starting process finished")

        dead_processes: list[str] = list()
        alive_process_count: int = len(self.service_bundles)
        for io_type_name, bundle in self.service_bundles.items():
            if not bundle.process.is_alive():
                dead_processes.append(io_type_name)
                alive_process_count -= 1

        try:
            while alive_process_count > 0:
                for io_type_name, source_bundle in self.service_bundles.items():
                    if io_type_name in dead_processes:
                        continue

                    if not source_bundle.process.is_alive():
                        print(f"Service '{io_type_name}' is dead")
                        dead_processes.append(io_type_name)
                        alive_process_count -= 1

                    self.dispatch_notifications(
                        io_type_name=io_type_name,
                        source_bundle=source_bundle,
                        dead_processes=dead_processes
                    )

                time.sleep(0.01)

        except KeyboardInterrupt:
            pass

        except Exception:
            raise

        finally:
            self.shutdown()

    def dispatch_notifications(self, io_type_name: str, source_bundle: ServiceBundle, dead_processes: list[str]):
        while not source_bundle.service.notification_queue_out.empty():
            # Avoid race condition
            if io_type_name in dead_processes:
                break

            notification = source_bundle.service.notification_queue_out.get()
            if self.verbose:
                value = notification.new_value if notification.new_value is not None else "None"
                print("{io} (scope={scope}) > {variable_name} = {value}".format(
                    io=io_type_name,
                    scope=notification.scope.value,
                    variable_name=notification.variable_name,
                    value=value
                ))

            if notification.scope == ChangeNotificationScope.Broadcast:
                for target_bundle in self.service_bundles.values():
                    target_bundle.service.notification_queue_in.put(notification)

            elif notification.scope == ChangeNotificationScope.Local:
                source_bundle.service.notification_queue_in.put(notification)

            elif notification.scope == ChangeNotificationScope.Foreign:
                for target_bundle in self.service_bundles.values():
                    if target_bundle == source_bundle:
                        continue
                    target_bundle.service.notification_queue_in.put(notification)

    def shutdown(self):
        for io_name, bundle in self.service_bundles.items():
            clear(bundle.service.notification_queue_out)
            clear(bundle.service.io_message_queue_out)
            clear(bundle.service.notification_queue_in)
            clear(bundle.service.io_message_queue_in)

            while bundle.process.is_alive():
                time.sleep(0.01)

            print(f"Process for Service '{io_name}' finished with code {bundle.process.exitcode}")
