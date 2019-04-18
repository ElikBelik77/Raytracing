from math import sqrt
from Vector import Vector



class Camera:
    def __init__(self, vFov, hFov, direction, view_distance):
        self.vFov = vFov
        self.hFov = hFov
        self.direction = direction
        self.view_distance = view_distance

    def getCameraGrid(self):
        cameraMidView = self.direction.normalize().scale(self.view_distance)

        vectors = []
        for i in range(0, self.vFov):
            for j in range(0, self.hFov):
                v = Vector(i - self.vFov / 2, j - self.hFov / 2, -self.view_distance)
                v = v.rotate(self.direction).scale(self.view_distance)
                vectors.append(v)

        return vectors

    def getRaycasts(self):
        pass
