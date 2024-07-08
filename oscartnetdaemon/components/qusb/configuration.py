from dataclasses import dataclass

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration


@dataclass
class QuSbConfiguration(BaseConfiguration):
    host: str
    port: int
