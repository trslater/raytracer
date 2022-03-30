import math
from raytracer.camera import Camera
from raytracer.geometry import Point3D, Parallelogram
from raytracer.rendering import Image
from raytracer.scene import Scene


def main():
    parallelogram = Parallelogram(
        Point3D(-1, 3, 0),
        Point3D(-2, 1, 0),
        Point3D(2, -1, 0))

    scene = Scene((parallelogram,))
    camera = Camera(10, 1, math.pi/4, 1, 100)
    image = Image(scene, camera, width=100)
    
    image.render()
    image.save("test")


if __name__ == "__main__":
    main()
