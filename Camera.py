from math import sqrt
from Vector import Vector
from numpy import linspace



class Camera:
    def __init__(self, vFov, hFov, density, direction, view_distance):
        self.vFov = vFov
        self.hFov = hFov
        self.direction = direction
        self.density = density
        self.view_distance = view_distance
        self.vertical_vector_count = self.vFov/self.density
        self.position = Vector(0,0,0)

    def getCameraGrid(self):
        vectors = []
        for i in linspace(0,self.vFov,self.vFov/self.density):
            for j in linspace(0,self.hFov,self.hFov/self.density):
                v = Vector(i - self.vFov / 2, j - self.hFov / 2, -self.view_distance)
                v = v.rotate(self.direction).scale(self.view_distance)
                vectors.append(v)
        print ('done generating grid')
        return vectors

    def getRaycasts(self):
        pass
