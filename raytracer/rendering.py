from functools import cached_property
import os
from datetime import datetime

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
        progress = Progress(self.width*self.height - 1)
        start_time = datetime.now()
        
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
                
                progress.update(i*self.width + j)

        if self.anti_aliasing:
            self.pixel_colors = self.downsample(self.pixel_colors)
        
        elapsed_time = datetime.now() - start_time
        print(f"Completed in {elapsed_time}")

    def save(self, file_name) -> None:
        Saver.fromarray(np.uint8(self.pixel_colors*255)).save(f"{file_name}.png")

    def downsample(self, pixel_colors):
        return (pixel_colors
                .reshape(self.height//4, 4, self.width//4, 4, 4)
                .mean(axis=(1, 3)))


class Progress:
    def __init__(self, max_value) -> None:
        # Options
        self.max_value = max_value
        self.width = min(os.get_terminal_size()[0] - 8, 50)

        # Init state
        self.percent_done = 0
        self.num_bars = -1
        self.old_num_bars = -1

    def update(self, value):
        self.percent_done = value/self.max_value
        num_bars = int(self.percent_done*self.width)

        # Only print changes
        if num_bars > self.num_bars:
            bars = "="*num_bars
            space = " "*(self.width - num_bars)

            print(f"{self.percent_done:4.0%} [{bars}>{space}]", end="\r")
        
        if self.percent_done == 1:
            print()
        
        self.num_bars = num_bars
