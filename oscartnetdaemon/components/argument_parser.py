import argparse
import logging

from oscartnetdaemon.core.configuration import Configuration

_logger = logging.getLogger(__name__)


def parse_args() -> Configuration:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a", "--artnet-target-nodes", nargs='+', default=["127.0.0.1"],
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
        "-m", "--midi-in-port", type=str, default="OSCArtnetLoopback 0",
        help="MIDI Port to listen for tempo"
    )

    parser.add_argument(
        "-n", "--midi-out-port", type=str, default="OSCArtnetLoopback 1",
        help="MIDI Port to send tap tempo"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Logs all OSC messages"
    )

    arguments, _ = parser.parse_known_args()

    return Configuration(
        is_verbose=arguments.verbose,
        artnet_target_nodes=arguments.artnet_target_nodes,
        artnet_universe=arguments.artnet_universe,
        midi_in_port=arguments.midi_in_port,
        midi_out_port=arguments.midi_out_port,
        osc_server_address=arguments.osc_server_address,
        osc_server_port=arguments.osc_server_port
    )
