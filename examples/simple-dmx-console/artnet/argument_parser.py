import argparse


def parse_command_line_args() -> list[str]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a", "--artnet-files", nargs='+', required=True,
        help="List of Artnet configuration files"
    )

    arguments, _ = parser.parse_known_args()

    return arguments.artnet_files
