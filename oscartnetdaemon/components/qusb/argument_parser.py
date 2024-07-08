import argparse


def parse_command_line_args() -> list[str]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-q", "--qu-sb", nargs='+', required=True,
        help="List of Qu-SB configuration files"
    )

    arguments, _ = parser.parse_known_args()

    return arguments.qu_sb
