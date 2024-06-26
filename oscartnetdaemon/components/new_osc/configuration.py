from dataclasses import dataclass

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration


@dataclass
class OSCConfiguration(BaseConfiguration):
    server_ip_address: str
    server_ip_address_autodetect: bool
    server_port: int
