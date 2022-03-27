from dataclasses import dataclass
from functools import cached_property
from math import sqrt
from numbers import Number

import numpy as np


class NoIntersection(Exception):
    pass


class Point2D:
    """Convenience wrapper for ndarray"""

    def __init__(self, x, y) -> None:
        self._data = np.array((x, y))

    @property
    def x(self):
        return self._data[0]

    @property
    def y(self):
        return self._data[1]

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

    def __array__(self, dtype=None):
        return self._data

    def __str__(self) -> str:
        return "(" + ", ".join(str(x) for x in self._data) + ")"

    def __repr__(self) -> str:
        return str(self)


class Point3D(Point2D):
    """Convenience wrapper for ndarray"""

    def __init__(self, x, y, z) -> None:
        self._data = np.array((x, y, z))

    @property
    def z(self):
        return self._data[2]

    def cross(self, other):
        return self.__class__(*np.cross(self._data, np.asarray(other)))


@dataclass(frozen=True)
class Ray:
    origin: Point3D
    direction: Point3D

    def point(self, t):
        return self.origin + t*self.direction

    def intersection(self, shape) -> float:
        if isinstance(shape, Sphere):
            a = self.direction.dot(self.direction)
            b = 2*(self.origin - shape.center).dot(self.direction)
            c = ((self.origin - shape.center).dot(self.origin - shape.center)
                - shape.radius**2)

            discriminant = b*b - 4*a*c

            # Misses sphere
            if discriminant < 0:
                raise NoIntersection()

            # Tangent to sphere surface
            if discriminant == 0:
                return -b/(2*a)

            # Goes through sphere, i.e., two intersections
            t1 = (-b + sqrt(discriminant))/(2*a)
            t2 = (-b - sqrt(discriminant))/(2*a)

            return min(t1, t2)

        elif isinstance(shape, Plane):
            return ((shape.position - self.origin).dot(shape.normal)
                    /(self.dot(shape.normal)))

        # Triangles and parallelograms are checked the same way, the 'in'
        # checking is just different
        elif isinstance(shape, Parallelogram) or isinstance(shape, Triangle):
            t = self.intersection(shape.plane())
            point = self.point(t)

            if point not in shape:
                raise NoIntersection()

            return t


@dataclass(frozen=True)
class Shape:
    pass


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

    def __contains__(self, p: Point3D) -> bool:
        raise NotImplemented()

    def plane(self):
        return Plane(self.origin, self.a.cross(self.b))


@dataclass(frozen=True)
class Triangle(Parallelogram):
    def __contains__(self, p: Point3D) -> bool:
        raise NotImplemented()
