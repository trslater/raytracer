from functools import cached_property

import numpy as np
from PIL import Image as Saver

from .camera import Camera
from .geometry import NoIntersection, Point3D, Ray
from .scene import Scene


class Image:
    def __init__(self, scene: Scene, camera: Camera,
                 width: int=None, height: int=None,
                 anti_aliasing=True) -> None:
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
        self.anti_aliasing = anti_aliasing
        
        if anti_aliasing:
            self.width *= 4
            self.height *= 4

        self.pixel_colors = np.ndarray((self.height, self.width, 4))

    def pixel_center(self, i, j) -> Point3D:
        shifted_i = i - (self.height - 1)/2
        shifted_j = (self.width - 1)/2 - j

        x = self.pixel_width*shifted_j
        y = self.pixel_height*shifted_i

        return Point3D(x, y, self.camera.position.z - self.camera.near_clip)

    @cached_property
    def pixel_width(self) -> float:
        return self.camera.near_clip_width/self.width

    @cached_property
    def pixel_height(self) -> float:
        return self.camera.near_clip_height/self.height

    def render(self) -> None:
        old_num_bars = -1
        
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
                        self.pixel_colors[i][j] = (1, 1, 1, 1)
                
                k = i*self.width + j
                percent_done = k/self.height/self.width
                total_bars = 100
                num_bars = int(total_bars*percent_done)

                # Only print changes
                if num_bars > old_num_bars:
                    print((f"{percent_done:4.0%} ["
                           + "="*num_bars + ">" + " "*(total_bars - num_bars - 1)),
                          end="]\r")
                
                old_num_bars = num_bars
        
        if self.anti_aliasing:
            self.pixel_colors = self.downsample(self.pixel_colors)

    def save(self, file_name) -> None:
        Saver.fromarray(np.uint8(self.pixel_colors*255)).save(f"{file_name}.png")

    def downsample(self, pixel_colors):
        return (pixel_colors
                .reshape(self.height//4, 4, self.width//4, 4, 4)
                .mean(axis=(1, 3)))
