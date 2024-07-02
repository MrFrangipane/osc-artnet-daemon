from dataclasses import dataclass

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration


@dataclass
class ArtnetConfiguration(BaseConfiguration):
    universe: int
    target_nodes: list[str]
