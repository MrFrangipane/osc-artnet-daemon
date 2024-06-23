from dataclasses import dataclass, field


@dataclass
class AbstractControlValue:
    pass


@dataclass
class FloatControlValue(AbstractControlValue):
    value: float = 0.0


@dataclass
class ColorControlValue(AbstractControlValue):
    h: float = 0.0
    s: float = 0.0
    l: float = 0.0


@dataclass
class AbstractControl:
    name: str
    value: AbstractControlValue


@dataclass
class FloatControl(AbstractControl):
    value: FloatControlValue = field(default_factory=FloatControlValue)


@dataclass
class ColorControl(AbstractControl):
    value: ColorControlValue = field(default_factory=ColorControlValue)
