from tkinter import *

class GameObject:
    def __init__(self, pos):
        self.pos = pos
        self.canvas_obj = None

    def draw(self, canvas):
        if self.canvas_obj != None:
            canvas.delete(self.canvas_obj)