import math


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2) if math.sqrt(
            self.x ** 2 + self.y ** 2 + self.z ** 2) != 0 else 1

    def normalize(self):
        mag = self.magnitude()
        return Vector(self.x / mag, self.y / mag, self.z / mag)

    def scale(self, scale):
        return Vector(self.x * scale, self.y * scale, self.z * scale)

    def add(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def rotate(self, angles):
        return self.rotateX(angles.x).rotateY(angles.y).rotateZ(angles.z)

    def rotateX(self, rad):
        """ Rotates the point around the X axis by the given angle in degrees. """

        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Vector(self.x, y, z)

    def rotateY(self, rad):
        """ Rotates the point around the Y axis by the given angle in degrees. """

        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Vector(x, self.y, z)

    def rotateZ(self, rad):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Vector(x, y, self.z)

    def distance(self, v):
        return math.sqrt((self.x - v.x) ** 2 + (self.y - v.y) ** 2 + (self.z - v.z) ** 2)

    def get_closest(self, points):
        min_distance = points[0].distance(self)
        min_point = points[0]
        for p in points:
            if p.distance(self) < min_distance:
                min_distance = p.distance(self)
                min_point = p

        return min_point

    def get_direction(self):
        return Vector(math.acos(self.x / self.magnitude()), math.acos(self.y / self.magnitude()),
                      math.acos(self.z / self.magnitude())).normalize()

    def multiply(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'
