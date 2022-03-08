from typing import NamedTuple
import numpy as np


class Point3D(NamedTuple):
    x: float
    y: float
    z: float

    def __array__(self):
        return np.array((self.x, self.y, self.z))
