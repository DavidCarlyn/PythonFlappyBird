from tkinter import *
from game_object import GameObject

GRAVITY = .5
MAX_DOWN_SPEED = 12
UP_BOOST = 10

class Bird(GameObject):
    def __init__(self, pos):
        super().__init__(pos)
        self.width = 50
        self.height = 50
        self.fly_speed = MAX_DOWN_SPEED

    def fly_up(self):
        self.fly_speed = -UP_BOOST

    def move(self):
        self.pos.y += self.fly_speed

        # Gravity accelerates
        if self.fly_speed < MAX_DOWN_SPEED:
            self.fly_speed = self.fly_speed + GRAVITY

    def draw(self, canvas):
        super().draw(canvas)
        self.canvas_obj = canvas.create_oval(
            self.pos.x, 
            self.pos.y, 
            self.pos.x + self.width, 
            self.pos.y + self.height,
            fill="yellow"
        )