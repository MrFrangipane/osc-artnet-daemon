import colorsys


def hsl_to_rgbw(h: float, s: float, l: float) -> [float, float, float, float]:
    r, g, b = colorsys.hls_to_rgb(h, l, s)

    max_ = float(max(r, max(g, b)))
    min_ = float(min(r, min(g, b)))

    if max_ == 0.0:
        return 0, 0, 0, 0

    if min_ / max_ < 0.5:
        white = (min_ * max_) / (max_ - min_)
    else:
        white = max_

    factor_ = (white + max_) / max_
    return (
        (factor_ * r) - white,
        (factor_ * g) - white,
        (factor_ * b) - white,
        white
    )
