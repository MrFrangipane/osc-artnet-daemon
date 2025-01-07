from dataclasses import dataclass

from dataclasses_json import dataclass_json

# FIXME use https://docs.python.org/3.10/library/ipaddress.html


@dataclass_json
@dataclass
class Configuration:
    is_verbose: bool
    artnet_target_nodes: list[str]
    artnet_universe: int
    midi_in_port: str
    midi_out_port: str
    osc_server_address: str
    osc_server_port: int
