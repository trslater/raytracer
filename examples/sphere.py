import math
from raytracer.camera import Camera
from raytracer.geometry import Point3D, Sphere
from raytracer.rendering import Image
from raytracer.scene import Scene


def main():
    sphere = Sphere(Point3D(0, 0, 0), 3)

    scene = Scene((sphere,))
    camera = Camera(10, 1, math.pi/4, 1, 100)
    image = Image(scene, camera, width=100)
    
    image.render()
    image.save("test")


if __name__ == "__main__":
    main()
