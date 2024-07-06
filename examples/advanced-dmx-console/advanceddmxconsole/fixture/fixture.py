from advanceddmxconsole.fixture.dmx_channel import DMXChannel
from advanceddmxconsole.fixture.fixture_info import FixtureInfo


class Fixture:

    def __init__(self, info: FixtureInfo):
        self.info: FixtureInfo = info
        self.universe_address: int = -1
        self.channels: list[DMXChannel] = list()

    def create_channels(self, universe_address: int):
        self.universe_address = universe_address

        self.channels = list()
        for channel_number, channel_info in enumerate(self.info.type.channels):
            value_default = float(channel_info.default_int) / 255.0
            new_channel = DMXChannel(
                name=channel_info.name,
                unused=channel_info.unused,
                value=value_default,
                value_default=value_default,
                channel_number=channel_number
            )
            self.channels.append(new_channel)
