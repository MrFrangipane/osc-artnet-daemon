import logging

from oscartnetdaemon.midi_osc_test_bridge.domain.service import Domain


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    domain = Domain()
    try:
        domain.start()
    except KeyboardInterrupt:
        pass
    domain.stop()
