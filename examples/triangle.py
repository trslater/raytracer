import math
from raytracer.camera import Camera
from raytracer.geometry import Point3D, Triangle
from raytracer.rendering import Image
from raytracer.scene import Scene


def main():
    triangle = Triangle(
        Point3D(0, 2, 0),
        Point3D(-2, -2, 0),
        Point3D(2, -2, 0))

    scene = Scene((triangle,))
    camera = Camera(10, 1, math.pi/4, 1, 100)
    image = Image(scene, camera, width=100)
    
    image.render()
    image.save("test")


if __name__ == "__main__":
    main()
