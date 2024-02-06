from oscartnetdaemon.core.components import Components


class MoodUpdater:
    def __init__(self):
        self._mood = Components().mood

    def update(self, address, values):

        if address == '/encoder1':
            self._mood.hue = values[0]

        elif address == '/encoder2':
            self._mood.saturation = values[0]

        elif address == '/encoder3':
            self._mood.value = values[0]
