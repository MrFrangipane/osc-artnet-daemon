from copy import copy

from advanceddmxconsole.fixture.dmx_channel import BaseDMXChannel, DMXChannel, DMXChannelFloat


class BaseFixtureDefinition:
    Channels: list[BaseDMXChannel] = list()

    def __init__(self):
        self.channels: list[BaseDMXChannel] = list()

    def create_channels(self, start_channel: int, skip_unused=True):
        channel_number = start_channel
        self.channels = list()

        for channel in self.Channels:
            if skip_unused and channel.unused:
                continue

            new_channel = copy(channel)
            new_channel.channel_number = channel_number
            self.channels.append(new_channel)

            if isinstance(channel, DMXChannelFloat):
                channel_number += 2
            else:
                channel_number += 1
