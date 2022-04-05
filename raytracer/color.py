import numpy as np


class Color:
    def __init__(self, r: float, g: float, b: float) -> None:
        self.data = np.clip(np.array((r, g, b)), 0, 1)

    @property
    def red(self) -> float:
        return self.data[0]

    @property
    def green(self) -> float:
        return self.data[1]

    @property
    def blue(self) -> float:
        return self.data[2]

    @classmethod
    def from_hsl(cls, h: float, s: float, l: float):
        raise NotImplementedError()

    @classmethod
    def from_hsv(cls, h: float, s: float, l: float):
        raise NotImplementedError()

    def __add__(self, other):
        return self.__class__(*(self.data + other.data))

    def __rmul__(self, scalar):
        return self.__class__(*(scalar*self.data))

    def __str__(self) -> str:
        return f"({self.red}, {self.green}, {self.blue}, {self.alpha})"
