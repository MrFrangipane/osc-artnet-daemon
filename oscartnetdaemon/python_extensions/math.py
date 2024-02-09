

def map_to_int(input_: float, min_: int = 0, max_: int = 255) -> int:
    return int(min_ + (max_ - min_) * input_)
