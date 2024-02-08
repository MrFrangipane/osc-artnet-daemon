import argparse
import logging
import socket

from oscartnetdaemon.core.configuration import Configuration

_logger = logging.getLogger(__name__)


def parse_args() -> Configuration:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a", "--artnet-target-node", default="127.0.0.1",
        help="Name or address of the Artnet target node"
    )

    parser.add_argument(
        "-u", "--artnet-universe", type=int, default=0,
        help="Number of the Artnet universe"
    )

    parser.add_argument(
        "-o", "--osc-server-address", default="0.0.0.0",
        help="IP Address the OSC server binds to"
    )

    parser.add_argument(
        "-p", "--osc-server-port", type=int, default="8080",
        help="Port the OSC server binds to"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Logs all OSC messages"
    )
    arguments = parser.parse_args()

    return Configuration(
        is_verbose=arguments.verbose,
        artnet_target_node_ip=socket.gethostbyname(arguments.artnet_target_node),
        artnet_universe=arguments.artnet_universe,
        osc_server_address=arguments.osc_server_address,
        osc_server_port=arguments.osc_server_port
    )
