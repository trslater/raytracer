import sys

from .geometry import Parallelogram, Plane, Ray, Sphere, Triangle


class NoIntersection(Exception):
    pass


def intersection(o1: Parallelogram|Plane|Ray|Sphere|Triangle,
                 o2: Parallelogram|Plane|Ray|Sphere|Triangle) -> float:
    o1_type = type(o1).__name__.lower()
    o2_type = type(o2).__name__.lower()
    
    function_name = f"{o1_type}_{o2_type}_intersection"
    current_module = sys.modules[__name__]

    function = getattr(current_module, function_name)

    return function(o1, o2)


# Parallelogram intersections
# -----------------------------------------------------------------------------


def parallelogram_parallelogram_intersection(pa1: Parallelogram,
                                             pa2: Parallelogram) -> float:
    raise NotImplemented()


def parallelogram_plane_intersection(pa: Parallelogram, pl: Plane) -> float:
    raise NotImplemented()


def parallelogram_ray_intersection(pa: Parallelogram, r: Ray) -> float:
    raise NotImplemented()


def parallelogram_sphere_intersection(pa: Parallelogram, s: Sphere) -> float:
    raise NotImplemented()


def parallelogram_triangle_intersection(pa: Parallelogram, t: Triangle) -> float:
    raise NotImplemented()


# Plane intersections
# -----------------------------------------------------------------------------


def plane_parallelogram_intersection(pl: Plane, pa: Parallelogram) -> float:
    return parallelogram_plane_intersection(pa, pl)


def plane_plane_intersection(pl1: Plane, pl2: Plane) -> float:
    raise NotImplemented()


def plane_ray_intersection(plane: Plane, ray: Ray) -> float:
    return ((plane.position - ray.origin).dot(plane.normal)
            /(ray.dot(plane.normal)))


def plane_sphere_intersection(pl: Plane, s: Sphere) -> float:
    raise NotImplemented()


def plane_triangle_intersection(pl: Plane, t: Triangle) -> float:
    raise NotImplemented()


# Ray intersections
# -----------------------------------------------------------------------------


def ray_parallelogram_intersection(r: Ray, pa: Parallelogram) -> float:
    return parallelogram_ray_intersection(pa, r)


def ray_plane_intersection(r: Ray, pl: Plane) -> float:
    return plane_ray_intersection(pl, r)


def ray_ray_intersection(r1: Ray, r2: Ray) -> float:
    raise NotImplemented()


def ray_sphere_intersection(r: Ray, s: Sphere) -> float:
    raise NotImplemented()


def ray_triangle_intersection(r: Ray, t: Triangle) -> float:
    raise NotImplemented()


# Sphere intersections
# -----------------------------------------------------------------------------


def sphere_parallelogram_intersection(s: Sphere, pa: Parallelogram) -> float:
    return parallelogram_sphere_intersection(pa, s)


def sphere_plane_intersection(s: Sphere, pl: Plane) -> float:
    return plane_sphere_intersection(pl, s)


def sphere_ray_intersection(s: Sphere, r: Ray) -> float:
    return ray_sphere_intersection(r, s)


def sphere_sphere_intersection(s1: Sphere, s2: Sphere) -> float:
    raise NotImplemented()


def sphere_triangle_intersection(s: Sphere, t: Triangle) -> float:
    raise NotImplemented()


# Triangle intersections
# -----------------------------------------------------------------------------


def triangle_parallelogram_intersection(t: Triangle, pa: Parallelogram) -> float:
    return parallelogram_triangle_intersection(pa, t)


def triangle_plane_intersection(t: Triangle, pl: Plane) -> float:
    raise plane_triangle_intersection(pl, t)


def triangle_ray_intersection(t: Triangle, r: Ray) -> float:
    return ray_triangle_intersection(r, t)


def triangle_sphere_intersection(t: Triangle, s: Sphere) -> float:
    return sphere_triangle_intersection(s, t)


def triangle_triangle_intersection(t1: Triangle, t2: Triangle) -> float:
    raise NotImplemented()
