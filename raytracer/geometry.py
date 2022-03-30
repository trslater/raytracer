from dataclasses import dataclass
from functools import cached_property
from math import sqrt
from numbers import Number

import numpy as np


class Colinear(Exception):
    pass


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
        return self.__class__(*(self._data + np.asarray(other)))

    def __sub__(self, other):
        return self.__class__(*(self._data - np.asarray(other)))

    def __mul__(self, scalar):
        if not isinstance(scalar, Number):
            raise ValueError("Only scalar multiplication allowed")
            
        return self.__class__(*(self._data*scalar))

    def __rmul__(self, scalar):
        return self*scalar

    def __truediv__(self, scalar):
        if not isinstance(scalar, Number):
            raise ValueError("Only scalar division allowed")
            
        return self.__class__(*(self._data/scalar))

    def dot(self, other):
        return np.dot(self._data, np.asarray(other))

    def component(self, other):
        return self.dot(other)/self.dot(self)

    def projection(self, other):
        return self.component(other)*self.normalized()

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
            return self._sphere_intersection(shape)

        if isinstance(shape, Plane):
            return self._plane_intersection(shape)

        if isinstance(shape, Polygon):
            return self._polygon_intersection(shape)

    def _sphere_intersection(self, sphere):
        a = self.direction.dot(self.direction)
        b = 2*(self.origin - sphere.center).dot(self.direction)
        c = ((self.origin - sphere.center).dot(self.origin - sphere.center)
            - sphere.radius**2)

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
    
    def _plane_intersection(self, plane):
        return ((plane.point - self.origin).dot(plane.normal)
                /(self.dot(plane.normal)))
    
    def _polygon_intersection(self, polygon):
        t = self.intersection(polygon.plane())
        point = self.point(t)

        # Each polygon provides its own point in polygon algorithm
        if point not in polygon:
            raise NoIntersection()

        return t


@dataclass(frozen=True)
class AxisAlignedBox:
    mined: Point3D
    maxed: Point3D


@dataclass(frozen=True)
class Sphere:
    center: Point3D
    radius: float

    def bounding_box(self) -> AxisAlignedBox:
        return AxisAlignedBox(
            self.center - Point3D(self.radius, self.radius, self.radius),
            self.center + Point3D(self.radius, self.radius, self.radius))


@dataclass(frozen=True)
class Plane:
    point: Point3D
    normal: Point3D


class Polygon:
    def __init__(self, *points: Point3D) -> None:
        if len(points) < 3:
            raise ValueError()

        self._points = points

    def plane(self):
        return Plane(self._points[0],
                     (self._points[1] - self._points[0])
                     .cross(self._points[2] - self._points[0]))

    def bounding_box(self) -> AxisAlignedBox:
        return AxisAlignedBox(
            Point3D(min(p.x for p in self._points),
                    min(p.y for p in self._points),
                    min(p.z for p in self._points)),
            Point3D(max(p.x for p in self._points),
                    max(p.y for p in self._points),
                    max(p.z for p in self._points)))


class Triangle(Polygon):
    def __init__(self, a: Point3D, b: Point3D, c: Point3D) -> None:
        self.a = a
        self.b = b
        self.c = c

        super().__init__(*(a, b, c))

    def uv(self, point):
        """This only works when point is already known to be in the plane of
        the triangle."""

        ab = self.b - self.a
        ac = self.c - self.a

        determinant = ab.x*ac.y - ab.y*ac.x

        # ab and ac are colinear
        if determinant == 0:
            raise Colinear("Vectors AB and AC are colinear")

        ap = point - self.a

        u = (ap.x*ac.y - ap.y*ac.x)/determinant
        v = (ab.x*ap.y - ab.y*ap.x)/determinant

        return u, v

    def __contains__(self, point: Point3D) -> bool:
        try:
            u, v = self.uv(point)
        
        except Colinear:
            return False

        return (0 <= u <= 1) and (0 <= v <= 1) and (0 <= 1 - u - v <= 1)


class Parallelogram(Triangle):
    @property
    def d(self):
        return self.b + self.c - self.a

    def __contains__(self, point: Point3D) -> bool:
        u, v = self.uv(point)

        return (0 <= u <= 1) and (0 <= v <= 1)
