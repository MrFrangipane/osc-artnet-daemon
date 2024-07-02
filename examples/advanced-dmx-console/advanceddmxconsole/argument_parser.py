import argparse


def parse_command_line_args() -> tuple[list[str], int, list[str]]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a", "--artnet-files", nargs='+', required=True,
        help="List of Artnet configuration files"
    )
    parser.add_argument(
        "-u", "--artnet-universe", required=True, type=int,
        help="Artnet universe number"
    )
    parser.add_argument(
        "-n", "--artnet-nodes", nargs='+', required=True,
        help="List of Artnet target nodes (IP or hostname)"
    )
    arguments, _ = parser.parse_known_args()

    return arguments.artnet_files, arguments.artnet_universe, arguments.artnet_nodes
