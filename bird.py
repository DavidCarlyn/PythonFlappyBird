from tkinter import *
from game_object import GameObject

class Bird(GameObject):
    def __init__(self, pos):
        super().__init__(pos)
        self.width = 50
        self.height = 50

    def draw(self, canvas):
        super().draw(canvas)
        self.canvas_obj = canvas.create_oval(
            self.pos.x, 
            self.pos.y, 
            self.pos.x + self.width, 
            self.pos.y + self.height,
            fill="yellow"
        )