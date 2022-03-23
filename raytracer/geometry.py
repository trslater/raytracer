from dataclasses import dataclass
from functools import cached_property
from numbers import Number

import numpy as np

from .intersections import intersection


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
    def magnitude(self):
        return np.linalg.norm(self._data)

    def normalized(self):
        return self.__class__(*(self._data/self.magnitude))

    def __add__(self, other):
        return self.__class__(self._data + np.asarray(other))

    def __sub__(self, other):
        return self.__class__(self._data - np.asarray(other))

    def __mul__(self, scalar):
        if not isinstance(scalar, Number):
            raise ValueError("Only scalar multiplication allowed")
            
        return self.__class__(*(self._data*scalar))

    def __rmul__(self, scalar):
        return self*scalar

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


@dataclass(frozen=True)
class Ray:
    origin: Point3D
    direction: Point3D

    def point(self, t):
        return self.origin + t*self.direction


@dataclass(frozen=True)
class Shape:
    def intersection(self, other) -> float:
        return intersection(self, other)


@dataclass(frozen=True)
class Sphere(Shape):
    center: Point3D
    radius: float


@dataclass(frozen=True)
class Plane(Shape):
    position: Point3D
    normal: Point3D


@dataclass(frozen=True)
class Parallelogram(Shape):
    origin: Point3D
    a: Point3D
    b: Point3D

    def contains(self, p: Point3D) -> bool:
        raise NotImplemented()

    def plane(self):
        return Plane(self.origin, self.a.cross(self.b))


@dataclass(frozen=True)
class Triangle(Parallelogram):
    def contains(self, p: Point3D) -> bool:
        raise NotImplemented()
