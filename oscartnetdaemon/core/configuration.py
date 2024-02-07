from dataclasses import dataclass

# FIXME use https://docs.python.org/3.10/library/ipaddress.html


@dataclass
class Configuration:
    is_verbose: bool
    artnet_target_node_ip: str
    artnet_universe: int
    osc_server_address: str
    osc_server_port: int
