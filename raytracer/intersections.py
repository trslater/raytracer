from __future__ import annotations
from math import sqrt
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .geometry import Parallelogram, Plane, Ray, Sphere, Triangle


class NoIntersection(Exception):
    pass


def intersection(object_1: Parallelogram|Plane|Ray|Sphere|Triangle,
                 object_2: Parallelogram|Plane|Ray|Sphere|Triangle) -> float:
    object_1_type = type(object_1).__name__.lower()
    object_2_type = type(object_2).__name__.lower()
    
    function_name = f"{object_1_type}_{object_2_type}_intersection"
    current_module = sys.modules[__name__]

    function = getattr(current_module, function_name)

    return function(object_1, object_2)


# Parallelogram intersections
# -----------------------------------------------------------------------------


def parallelogram_parallelogram_intersection(
        parallelogram1: Parallelogram,
        parallelogram2: Parallelogram) -> float:
    raise NotImplemented()


def parallelogram_plane_intersection(parallelogram: Parallelogram,
                                     plane: Plane) -> float:
    raise NotImplemented()


def parallelogram_ray_intersection(parallelogram: Parallelogram,
                                   ray: Ray) -> float:
    plane = parallelogram.plane()
    t = plane_ray_intersection(plane, ray)
    point = ray.point(t)

    if not parallelogram.contains(point):
        raise NoIntersection()

    return t


def parallelogram_sphere_intersection(parallelogram: Parallelogram,
                                      sphere: Sphere) -> float:
    raise NotImplemented()


def parallelogram_triangle_intersection(parallelogram: Parallelogram,
                                        triangle: Triangle) -> float:
    raise NotImplemented()


# Plane intersections
# -----------------------------------------------------------------------------


def plane_parallelogram_intersection(plane: Plane,
                                     parallelogram: Parallelogram) -> float:
    return parallelogram_plane_intersection(parallelogram, plane)


def plane_plane_intersection(plane_1: Plane, plane_2: Plane) -> float:
    raise NotImplemented()


def plane_ray_intersection(plane: Plane, ray: Ray) -> float:
    return ((plane.position - ray.origin).dot(plane.normal)
            /(ray.dot(plane.normal)))


def plane_sphere_intersection(plane: Plane, sphere: Sphere) -> float:
    raise NotImplemented()


def plane_triangle_intersection(plane: Plane, triangle: Triangle) -> float:
    raise NotImplemented()


# Ray intersections
# -----------------------------------------------------------------------------


def ray_parallelogram_intersection(ray: Ray,
                                   parallelogram: Parallelogram) -> float:
    return parallelogram_ray_intersection(parallelogram, ray)


def ray_plane_intersection(ray: Ray, plane: Plane) -> float:
    return plane_ray_intersection(plane, ray)


def ray_sphere_intersection(ray: Ray, sphere: Sphere) -> float:
    a = ray.direction.dot(ray.direction)
    b = 2*(ray.origin - sphere.center).dot(ray.direction)
    c = ((ray.origin - sphere.center).dot(ray.origin - sphere.center)
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


def ray_triangle_intersection(ray: Ray, triangle: Triangle) -> float:
    plane = triangle.plane()
    t = plane_ray_intersection(plane, ray)
    point = ray.point(t)

    if not triangle.contains(point):
        raise NoIntersection()

    return t


# Sphere intersections
# -----------------------------------------------------------------------------


def sphere_parallelogram_intersection(sphere: Sphere,
                                      parallelogram: Parallelogram) -> float:
    return parallelogram_sphere_intersection(parallelogram, sphere)


def sphere_plane_intersection(sphere: Sphere, plane: Plane) -> float:
    return plane_sphere_intersection(plane, sphere)


def sphere_ray_intersection(sphere: Sphere, ray: Ray) -> float:
    return ray_sphere_intersection(ray, sphere)


def sphere_sphere_intersection(sphere_1: Sphere, sphere_2: Sphere) -> float:
    raise NotImplemented()


def sphere_triangle_intersection(sphere: Sphere, triangle: Triangle) -> float:
    raise NotImplemented()


# Triangle intersections
# -----------------------------------------------------------------------------


def triangle_parallelogram_intersection(triangle: Triangle,
                                        parallelogram: Parallelogram) -> float:
    return parallelogram_triangle_intersection(parallelogram, triangle)


def triangle_plane_intersection(triangle: Triangle, plane: Plane) -> float:
    raise plane_triangle_intersection(plane, triangle)


def triangle_ray_intersection(triangle: Triangle, ray: Ray) -> float:
    return ray_triangle_intersection(r, triangle)


def triangle_sphere_intersection(triangle: Triangle, sphere: Sphere) -> float:
    return sphere_triangle_intersection(sphere, triangle)


def triangle_triangle_intersection(triangle_1: Triangle,
                                   triangle_2: Triangle) -> float:
    raise NotImplemented()
