import argparse


def parse_command_line_args() -> list[str]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t", "--template-files", nargs='+', required=True,
        help="List of Template configuration files"
    )

    arguments, _ = parser.parse_known_args()

    return arguments.template_files
