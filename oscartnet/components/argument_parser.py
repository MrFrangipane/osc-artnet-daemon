import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a", "--artnet-target-ip", default="127.0.0.1",
        help="Name or address of the Artnet target node"
    )

    parser.add_argument(
        "-u", "--artnet-universe", type=int, default=0,
        help="Number of the ArtNet universe"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Logs all OSC messages"
    )

    return parser.parse_args()
