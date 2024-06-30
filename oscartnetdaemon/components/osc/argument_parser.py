import argparse


def parse_command_line_args() -> list[str]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-o", "--osc-files", nargs='+', required=True,
        help="List of OSC configuration files"
    )

    arguments, _ = parser.parse_known_args()

    return arguments.osc_files
