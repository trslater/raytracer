from dataclasses import dataclass
from functools import cached_property
from math import tan

from .geometry import Plane, Point3D


@dataclass(frozen=True)
class Camera:
    """Near/far clip should be magnitudes. They will be """
    
    position: Point3D
    aspect: float
    vfov: float
    near_clip: float
    far_clip: float

    @cached_property
    def image_height(self) -> float:
        return 2*self.near_clip*tan(self.vfov/2)

    @cached_property
    def image_width(self) -> float:
        return self.image_height*self.aspect

    @cached_property
    def image_origin(self):
        # For now, to simplify, camera always looks in negative z direction
        # Origin in center of image
        return Point3D(self.position.x, self.position.y,
                       self.position.z - self.near_clip)

    @cached_property
    def near_plane(self) -> Plane:
        return Plane(self.image_origin, Point3D(0, 0, -1))

    @cached_property
    def far_plane(self) -> Plane:
        return Plane(Point3D(self.position.x, self.position.y,
                             self.position.z - self.far_clip),
                     Point3D(0, 0, -1))
