import logging

from advanceddmxconsole.gui.gui import GUI


if __name__ == '__main__':
    gui = GUI()

    # FIXME: LoggerWidget must exist before logging.Basic ?
    logging.basicConfig(level=logging.INFO)

    gui.exec()
