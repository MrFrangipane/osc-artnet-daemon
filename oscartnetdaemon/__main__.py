import logging
import time

from oscartnetdaemon.components.osc.components import OSCComponents


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    osc_components = OSCComponents()
    osc_components.initialize_from_file('./resources/template-widgets-mapping.yml')
    osc_components.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
