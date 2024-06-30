import argparse


def parse_command_line_args() -> list[str]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m", "--midi-files", nargs='+', required=True,
        help="List of MIDI configuration files"
    )

    arguments, _ = parser.parse_known_args()

    return arguments.midi_files
