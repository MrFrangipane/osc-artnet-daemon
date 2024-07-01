from simpledmxconsole.fixture.dmx_channel import DMXChannel


class BaseFixtureDefinition:
    Channels: list[DMXChannel] = list()
