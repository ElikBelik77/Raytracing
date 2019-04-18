from Vector import Vector
from math import sqrt

class Sphere:
    def __init__(self,x,y,z,r):
        self.center = Vector(x,y,z)
        self.r = r

    def distance(self, v : Vector):
        return sqrt((self.x-v.x)**2+(self.y-v.y)**2+(self.z-v.z)**2)

    def get_collision(self, v : Vector):
        a = v.get_direction().magnitude()**2
        c = self.center.magnitude()**2 - self.r**2
        b = 2 * (v.get_direction().multiply(self.center.scale(-1)))
        if b**2-4*a*c < 0:
            return None
        elif b**2 -4*a*c == 0:
            return [v.get_direction().scale([-b/2])]
        else:
            discriminant = sqrt((b**2)/4 - c)
            return [v.get_direction().scale(-b/2 + discriminant),v.get_direction().scale(-b/2-discriminant)]
