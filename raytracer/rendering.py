from functools import cached_property

import numpy as np
from PIL import Image as Saver

from .camera import Camera
from .geometry import NoIntersection, Point3D, Ray
from .scene import Scene


class Image:
    def __init__(self, scene: Scene, camera: Camera,
                 width: int=None, height: int=None) -> None:
        if width != None and height != None:
            raise ValueError("Can only specify height or width, not both")

        if width != None:
            height = width/camera.aspect

        if height != None:
            width = height*camera.aspect

        self.scene = scene
        self.camera = camera
        self.width = int(width)
        self.height = int(height)

        self.pixel_colors = np.ndarray((self.height, self.width, 4))

    def pixel_center(self, i, j) -> Point3D:
        x = self.pixel_width*((self.width - 1)/2 - j)
        y = self.pixel_height*((self.height - 1)/2 - i)

        return Point3D(x, y, self.camera.position.z - self.camera.near_clip)

    @cached_property
    def pixel_width(self) -> float:
        return self.camera.near_clip_width/self.width

    @cached_property
    def pixel_height(self) -> float:
        return self.camera.near_clip_height/self.height

    def render(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                ray_direction = (self.pixel_center(i, j)
                                 - self.camera.position).normalized()
                ray = Ray(self.camera.position, ray_direction)

                for obj in self.scene.objects:
                    try:
                        t = ray.intersection(obj)
                    
                    except NoIntersection:
                        self.pixel_colors[i][j] = (0, 0, 0, 0)

                    else:
                        self.pixel_colors[i][j] = (0, 0, 0, 1)

    def save(self, file_name) -> None:
        corrected_pixel_colors = np.uint8(self.pixel_colors*255)

        Saver.fromarray(corrected_pixel_colors).save(f"{file_name}.png")
