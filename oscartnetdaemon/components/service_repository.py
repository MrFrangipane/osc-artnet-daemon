import time
from multiprocessing import Process
from typing import Type

from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.service import Service
from oscartnetdaemon.domain_contract.service_bundle import ServiceBundle


class ServiceRepository:

    def __init__(self):
        self.service_bundles: dict[str, ServiceBundle] = dict()

    def register(self, registerer: Type[AbstractServiceRegisterer]):
        registration_info = registerer.make_registration_info()
        new_bundle = ServiceBundle(service=Service(registration_info))
        self.service_bundles[registration_info.io_type.__name__] = new_bundle

    def exec(self):
        for bundle in self.service_bundles.values():
            bundle.process = Process(target=bundle.service.exec)
            bundle.process.start()
            print(f"Starting service '{bundle.service.io_type.__name__}'...")
            while not bundle.service.startup_done.is_set():
                time.sleep(.1)

        dead_processes: list[str] = list()
        alive_process_count: int = len(self.service_bundles)
        try:
            while alive_process_count > 0:
                for io_type_name, source_bundle in self.service_bundles.items():
                    if io_type_name in dead_processes:
                        continue

                    if not source_bundle.process.is_alive():
                        print(f"Service with IO '{io_type_name}' is dead")
                        dead_processes.append(io_type_name)
                        alive_process_count -= 1

                    while not source_bundle.service.notification_queue_out.empty():
                        # Avoid race condition
                        if io_type_name in dead_processes:
                            break

                        notification = source_bundle.service.notification_queue_out.get()
                        for target_bundle in self.service_bundles.values():
                            target_bundle.service.notification_queue_in.put(notification)

                time.sleep(0.01)

        except KeyboardInterrupt:
            pass

        except Exception:
            raise

        finally:
            self.shutdown()

    def shutdown(self):
        for io_name, bundle in self.service_bundles.items():
            while bundle.process.is_alive():
                time.sleep(0.01)

            print(f"Process for Service with IO '{io_name}' has exited with code {bundle.process.exitcode}")
