from functools import cached_property

import numpy as np


class Point3D:
    """Convenience wrapper for ndarray"""

    def __init__(self, x, y, z) -> None:
        self._data = np.array((x, y, z))

    @property
    def x(self):
        return self._data[0]

    @property
    def y(self):
        return self._data[1]

    @property
    def z(self):
        return self._data[2]

    @cached_property
    def norm(self):
        return np.linalg.norm(self._data)

    @cached_property
    def normalized(self):
        return self.__class__(*(self._data/self.norm))

    def dot(self, other):
        return np.dot(self._data, np.asarray(other))

    def cross(self, other):
        return self.__class__(*np.cross(self._data, np.asarray(other)))

    def __array__(self, dtype=None):
        return self._data

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return str(self)
