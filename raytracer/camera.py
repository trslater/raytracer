from dataclasses import dataclass
from functools import cached_property
from math import tan

from .geometry import Plane, Point2D, Point3D


@dataclass(frozen=True)
class Camera:
    """Near/far clip should be magnitudes. They will be """
    
    distance: float
    aspect: float
    vfov: float
    near_clip: float
    far_clip: float

    @cached_property
    def position(self) -> Point3D:
        return Point3D(0, 0, -self.distance)

    @cached_property
    def near_clip_height(self) -> float:
        return 2*self.near_clip*tan(self.vfov/2)

    @cached_property
    def near_clip_width(self) -> float:
        return self.near_clip_height*self.aspect
