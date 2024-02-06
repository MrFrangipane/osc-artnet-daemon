import time
import math

from oscartnet.core.base_fixture import BaseFixture
from oscartnet.core.mood import Mood


class OnePixel(BaseFixture):

    def __init__(self, address):
        BaseFixture.__init__(self, address)
        self.channels = bytearray(3)

    def update(self, mood: Mood):
        self.channels[0] = int((mood.hue * math.cos(time.time()) * 0.5 + 0.5) * 255)
        self.channels[1] = int(mood.saturation * 255)
        self.channels[2] = int(mood.value * 255)
