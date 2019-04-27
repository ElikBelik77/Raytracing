import tkinter as tk
from Camera import Camera
from Vector import Vector
from math import pi
from Sphere import Sphere
import operator
import time

pressed_keys = set()


class Scene(tk.Frame):
    def __init__(self, width, height, master=None):
        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(master, width=width, height=height, bd=0, highlightthickness=0)
        self.screen_width = width
        self.screen_height = height
        self.canvas.pack()
        self.drawing_center = (750, 400)
        self.camera = Camera(1, 1, 0.01, Vector(3.6101425001453338,0.48253562503633296,0.0), 10)
        self.cameraGrid = []

        self.vision_rectangles = []
        master.bind("<KeyPress>", on_key_press)
        master.bind("<KeyRelease>", on_key_release)

    def draw_camera_vectors(self, objects):
        self.canvas.delete("all")
        camera_points = self.camera.getCameraGrid()

        for p in camera_points:
            intersects = False
            for object in objects:
                collisions = object.get_collision(p)
                if object.get_collision(p) is not None:
                    intersects = True
                    break
            if not intersects:
                self.cameraGrid.append(

                    self.canvas.create_line(self.drawing_center[0], self.drawing_center[1],
                                            self.drawing_center[0] + p.x, self.drawing_center[1] + p.y))

        self.camera.direction = self.camera.direction.modulus_add(Vector(0.08, 0, 0), Vector(2 * pi, 2 * pi, 2 * pi))
        self.canvas.after(1, self.draw_camera_vectors, objects)  # (time_delay, method_to_execute)

    def draw_axis(self):
        rotation = Vector(2 * pi / 8, 7 * pi / 8, pi / 2)
        y_axis = Vector(0, 1000, 0).rotate(rotation)
        x_axis = Vector(1000, 0, 0).rotate(rotation)
        z_axis = Vector(0, 0, 1000).rotate(rotation)
        lines = [x_axis, y_axis, z_axis]
        for line in lines:
            self.canvas.create_line(self.drawing_center[0], self.drawing_center[1], self.drawing_center[0] + line.x,
                                    self.drawing_center[1] + line.y)
        self.canvas.after(1, self.draw_axis)  # (time_delay, method_to_execute)

    def draw_vision(self, objects):
        camera_points = self.camera.getCameraGrid()
        count = 0
        tile_width = self.screen_width / self.camera.vertical_vector_count
        tile_height = self.screen_height / self.camera.vertical_vector_count

        if len(self.vision_rectangles) < len(camera_points):
            for i in range(0, len(camera_points)):
                x = i % self.camera.vertical_vector_count
                y = i // self.camera.vertical_vector_count
                self.vision_rectangles.append(
                    self.canvas.create_rectangle(x * tile_width, y * tile_height, (x + 1) * tile_width,
                                                 (y + 1) * tile_height, fill='black'))
        distance_dictionary = {}
        for p in camera_points:
            intersects = False
            closest_collision = None
            closest_object = None
            for object in objects:
                collisions = object[0].get_collision(p)
                if collisions is not None:
                    intersects = True
                    if closest_collision is None:
                        closest_collision = p.get_closest(collisions)
                        closest_object = object
                    if closest_collision is not None and p.distance(p.get_closest(collisions)) < p.distance(
                            closest_collision):
                        closest_collision = p.get_closest(collisions)
                        closest_object = object
            x = count % self.camera.vertical_vector_count
            y = count // self.camera.vertical_vector_count
            if not intersects:
                distance_dictionary[(x, y)] = (None,None)
            else:
                distance_dictionary[(x, y)] = (1/p.distance(closest_collision)**20,closest_object)
            count += 1


        max_distance = 0
        for p in distance_dictionary.keys():
            if distance_dictionary[p][0] is not None and distance_dictionary[p][0] > max_distance:
                max_distance = distance_dictionary[p][0]
        count = 0
        for p in distance_dictionary.keys():
            x = count % self.camera.vertical_vector_count
            y = count // self.camera.vertical_vector_count
            drawing_color = 'black' if distance_dictionary[p][0] is None else '#%02X%02X%02X' % (
            min(255, distance_dictionary[p][1][1][0] + int(255 * distance_dictionary[p][0] / max_distance)), min(255,distance_dictionary[p][1][1][1]+ int(255 * distance_dictionary[p][0] / max_distance)),
            min(255, distance_dictionary[p][1][1][2] + int(255 * distance_dictionary[p][0] / max_distance)))
            if self.canvas.itemcget(self.vision_rectangles[count], 'fill') != drawing_color:
                self.canvas.delete(self.vision_rectangles[count])
                self.vision_rectangles[count] = self.canvas.create_rectangle(x * tile_width, y * tile_height,
                                                                             (x + 1) * tile_width,
                                                                             (y + 1) * tile_height, fill=drawing_color,
                                                                             outline=drawing_color)
            count += 1

    def apply_user_input(self):
        if 'a' in pressed_keys:
            self.camera.direction = self.camera.direction.modulus_add(Vector(0.08, 0, 0),
                                                                      Vector(2 * pi, 2 * pi, 2 * pi))
        if 'd' in pressed_keys:
            self.camera.direction = self.camera.direction.modulus_add(Vector(-0.08, 0, 0),
                                                                      Vector(2 * pi, 2 * pi, 2 * pi))
        if 'w' in pressed_keys:

            self.camera.direction = self.camera.direction.modulus_add(Vector(0, 0.08, 0),
                                                                      Vector(2 * pi, 2 * pi, 2 * pi))
            print(self.camera.direction)
        if 's' in pressed_keys:
            self.camera.direction = self.camera.direction.modulus_add(Vector(0, -0.08, 0),
                                                                      Vector(2 * pi, 2 * pi, 2 * pi))
        if 'Up' in pressed_keys:
            self


def on_key_press(event):
    pressed_keys.add(event.keysym)


def on_key_release(event):
    pressed_keys.remove(event.keysym)


s = Scene(1500, 800, master=tk.Tk())
objects = [(Sphere(2, 7, 0, 3), (70, 0,0))]

while True:
    start_time = int(round(time.time() * 1000))
    s.draw_vision(objects)
    s.apply_user_input()
    s.update()
    end_time = int(round(time.time() * 1000))
    print(end_time - start_time)
    if 60 > end_time - start_time:
        time.sleep((60 - end_time + start_time) / 1000)
