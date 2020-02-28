from tkinter import *
from game_object import GameObject

class Pipe(GameObject):
    def __init__(self, pos):
        super().__init__(pos)
        self.width = 60
        self.height = 1000

    def draw(self, canvas):
        super().draw(canvas)
        self.canvas_obj = canvas.create_rectangle(
            self.pos.x,
            self.pos.y,
            self.pos.x + self.width,
            self.pos.y + self.height,
            fill="green"
        )