from abc import ABC, abstractmethod

from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo


class AbstractServiceRegisterer(ABC):
    """
    TODO will probably become a 'configurator' that also declares argparse arguments
    """

    @staticmethod
    @abstractmethod
    def make_registration_info() -> ServiceRegistrationInfo:
        pass
