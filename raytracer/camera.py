from dataclasses import dataclass
from functools import cached_property
from math import tan

from .geometry import Point3D


@dataclass(frozen=True)
class Camera:
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
        # For now, to simplify, camera always looks in positive z direction
        return Point3D(self.position.x - self.image_width/2,
                       self.position.y + self.image_height/2,
                       self.position.z + self.near_clip)
