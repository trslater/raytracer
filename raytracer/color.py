from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    red: float
    green: float
    blue: float
    alpha: float

    def __iter__(self) -> tuple[float]:
        return (self.red, self.green, self.blue, self.alpha)
