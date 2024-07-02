from copy import copy

from advanceddmxconsole.fixture.dmx_channel import BaseDMXChannel, DMXChannel, DMXChannelFloat


class BaseFixtureDefinition:
    Channels: list[BaseDMXChannel] = list()

    def __init__(self, name: str):
        self.name = name
        self.universe_address: int = -1
        self.channels: list[BaseDMXChannel] = list()

    def create_channels(self, universe_address: int, skip_unused=True):
        self.universe_address = universe_address

        channel_number = 0

        self.channels = list()
        for channel in self.Channels:
            new_channel = copy(channel)
            new_channel.channel_number = channel_number
            self.channels.append(new_channel)
            channel_number += 1
