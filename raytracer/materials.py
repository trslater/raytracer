from dataclasses import dataclass

from .color import Color


@dataclass(frozen=True)
class Material:
    color: Color
    diffusion: float
    specularity: float
    shininess: float
    opacity: float
