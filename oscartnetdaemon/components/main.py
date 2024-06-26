from multiprocessing import Process

from oscartnetdaemon.domain_contract.service import Service
from oscartnetdaemon.domain_contract.service_bundle import ServiceBundle
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo


class Main:

    def __init__(self):
        self.service_bundles: dict[str, ServiceBundle] = dict()

    def register_io_service(self, registration_info: ServiceRegistrationInfo):
        new_bundle = ServiceBundle(service=Service(registration_info))
        self.service_bundles[registration_info.io_type.__name__] = new_bundle

    def exec(self):
        for bundle in self.service_bundles.values():
            bundle.service.initialize()

        for bundle in self.service_bundles.values():
            bundle.process = Process(target=bundle.service.exec)
            bundle.process.start()

        try:
            while True:
                for source_bundle in self.service_bundles.values():
                    while not source_bundle.service.notifications_queue_out.empty():
                        notification = source_bundle.service.notifications_queue_out.get()
                        for target_bundle in self.service_bundles.values():
                            target_bundle.service.notification_queue_in.put(notification)

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        for io_name, bundle in self.service_bundles.items():
            bundle.process.kill()
            while bundle.process.is_alive():
                pass
            print(f"Process for Service with IO '{io_name}' has exited with code {bundle.process.exitcode}")
