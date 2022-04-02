import numpy as np


class Color:
    def __init__(self, r: float, g: float, b: float, a: float) -> None:
        self.data = np.array((r, g, b, a))

    @property
    def red(self) -> float:
        return self.data[0]

    @property
    def green(self) -> float:
        return self.data[1]

    @property
    def blue(self) -> float:
        return self.data[2]

    @property
    def alpha(self) -> float:
        return self.data[3]
