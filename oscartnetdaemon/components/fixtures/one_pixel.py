import time
import math

from oscartnetdaemon.core.base_fixture import BaseFixture
from oscartnetdaemon.core.mood import Mood


class OnePixel(BaseFixture):

    def __init__(self, address=0):
        BaseFixture.__init__(self, address)
        self._channels = bytearray(3)

    def update(self, mood: Mood, group_position: float = 0):
        self.channels[0] = int((mood.palette * math.cos(time.time() + group_position * 3.14) * 0.5 + 0.5) * 255)
        self.channels[1] = 0
        self.channels[2] = 0
