from raytracer.camera import Camera
from raytracer.geometry import Point3D, Sphere
from raytracer.rendering import Image
from raytracer.scene import Scene


def main():
    s = Scene((Sphere(Point3D(0, 0, 0), 3),))
    c = Camera(Point3D(0, 0, 5), 1, 45, 1, 100)
    i = Image(s, c, width=100)
    
    i.render()
    i.save("test")


if __name__ == "__main__":
    main()
