from tkinter import *
from bird import Bird
from pipe import Pipe
from pos import Pos
from tkinter import messagebox

import time
import random

GRAVITY = .5
MAX_DOWN_SPEED = 12
UP_BOOST = 10
PIPE_SPEED = 5
PIPE_FREQUENCY = 90
PIPE_GAP = 200
SCORE_FREQUENCY = 60
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000
CANVAS_UPDATE_SPEED = 1000//60

class flappy_bird(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.update()
        random.seed(time.time())

    def fly_up(self, event):
        print("HERE")
        self.fly_speed = -UP_BOOST    

    def create_widgets(self):
        self.score_lbl_str = StringVar(self)
        Label(self, textvariable=self.score_lbl_str, anchor="center", justify=CENTER).pack()
        self.score = 0
        self.score_lbl_str.set(f"Score : {self.score}")
        self.canvas = Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.bind("<Button-1>", self.fly_up) 
        self.canvas.pack()


        self.bird = Bird(Pos(50, 50))
        self.pipes = []
        self.fly_speed = 7
        self.counter = 0
        self.lost = False

    def create_piping(self):
        gap_height = random.randrange(CANVAS_HEIGHT-400)

        self.pipes.append(Pipe(Pos(CANVAS_WIDTH, gap_height-1000)))
        self.pipes.append(Pipe(Pos(CANVAS_WIDTH, gap_height + PIPE_GAP)))

    def check_collisions(self):
        bird_bottom = self.bird.pos.y + self.bird.height
        bird_top = self.bird.pos.y
        bird_left = self.bird.pos.x
        bird_right = self.bird.pos.x + self.bird.width

        if bird_bottom > CANVAS_HEIGHT:
            return True

        for pipe in self.pipes:
            pipe_bottom = pipe.pos.y + pipe.height
            pipe_top = pipe.pos.y
            pipe_left = pipe.pos.x
            pipe_right = pipe.pos.x + pipe.width
            if pipe_left > bird_right:
                continue
            if pipe_right < bird_left:
                continue
            if pipe_top > bird_bottom:
                continue
            if pipe_bottom < bird_top:
                continue
            #print(f"Bird: ({bird_left}, {bird_top}) - ({bird_right}, {bird_bottom})")
            #print(f"Pipe: ({pipe_left}, {pipe_top}) - ({pipe_right}, {pipe_bottom})")
            return True

        return False

    def update(self):
        # Bird update
        self.bird.pos.y += self.fly_speed
        if self.bird.pos.y < 0:
            self.bird.pos.y = 0
        self.bird.draw(self.canvas)

        # Pipe update
        pipes_to_remove = []
        for pipe in self.pipes:
            pipe.pos.x -= PIPE_SPEED
            pipe.draw(self.canvas)
            if pipe.pos.x + pipe.width < 0:
                pipes_to_remove.append(pipe)
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
            self.canvas.delete(pipe)

        # Check Collisions
        if self.check_collisions():
            self.lost = True

        # Gravity accelerates
        if self.fly_speed < MAX_DOWN_SPEED:
            self.fly_speed = self.fly_speed + GRAVITY

        # Produce pipes regularly
        self.counter += 1
        if self.counter % SCORE_FREQUENCY == 0:
            self.score += 1
            self.score_lbl_str.set(f"Score : {self.score}")
        if self.counter >= PIPE_FREQUENCY:
            self.counter = 0
            self.create_piping()

        # Update again
        if (not self.lost):
            self.canvas.after(CANVAS_UPDATE_SPEED, self.update)
        else:
            response = messagebox.askyesno("Restart Game", "Play Again?")
            if response == 1:
                self.pack_forget()
                new_app = flappy_bird(master=self.master)
                new_app.mainloop()
                self.destroy()
            else:
                self.destroy()
                self.master.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Flappy Bird")
    app = flappy_bird(master=root)
    app.mainloop()