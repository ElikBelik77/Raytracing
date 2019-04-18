import tkinter as tk
from Camera import Camera
from Vector import Vector
from math import pi
from Sphere import Sphere


class Scene(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(master, width=1500, height=800, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.drawing_center = (750,400)
        self.camera = Camera(10, 10, Vector(1, 1, 1).normalize(), 30)
        self.cameraGrid = []

    def drawCameraGrid(self):
        self.canvas.delete("all")
        camera_points = self.camera.getCameraGrid()
        s = Sphere(90,110,0,30)
        for p in camera_points:
            collisions = s.get_collision(p)
            if s.get_collision(p) is None:

                self.cameraGrid.append(

                    self.canvas.create_line(self.drawing_center[0], self.drawing_center[1], self.drawing_center[0]+p.x, self.drawing_center[1]+p.y))
            else:
                print("hit")
                p = Vector(0,0,0).get_closest(collisions)
                self.canvas.create_oval(self.drawing_center[0]+p.x-2,self.drawing_center[1] + p.y -2 ,self.drawing_center[0]+p.x+2,self.drawing_center[1] + p.y + 2 )

        self.camera.direction = self.camera.direction.add(Vector(0,-0.4,0))
        self.canvas.after(1, self.drawCameraGrid)  # (time_delay, method_to_execute)


s = Scene()
s.drawCameraGrid()
while True:
    s.update_idletasks()
    s.update()
