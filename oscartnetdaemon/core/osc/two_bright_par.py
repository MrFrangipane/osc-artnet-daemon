from dataclasses import dataclass, field


# fixme: factorize with Mapping ?
@dataclass
class HSL:
    h: int = 0
    s: int = 0
    l: int = 0


@dataclass
class TwoBrightPar:
    pars: list[HSL] = field(default_factory=lambda: [HSL(), HSL(), HSL(), HSL()])
