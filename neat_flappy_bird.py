from tkinter import *
from bird import Bird
from pipe import Pipe
from pos import Pos
from tkinter import messagebox

import neat

import time
import random
import os

PIPE_SPEED = 5
PIPE_FREQUENCY = 90
PIPE_GAP = 200
SCORE_FREQUENCY = 60
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000
CANVAS_UPDATE_SPEED = 1000//60

class flappy_bird(Frame):
    def __init__(self, genomes, config, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        random.seed(time.time())
        self.start(genomes, config)
    
    def start(self, genomes, config):
        self.create_widgets(genomes, config)
        self.update()

    def create_widgets(self, genomes, config):
        self.score_lbl_str = StringVar(self)
        Label(self, textvariable=self.score_lbl_str, anchor="center", justify=CENTER).pack()
        self.score = 0
        self.score_lbl_str.set(f"Score : {self.score}")
        self.canvas = Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack()

        self.pipes = []
        self.create_piping()
        self.counter = 0
        self.lost = False

        self.nets = []
        self.ge = []
        self.birds = []

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            self.birds.append(Bird(Pos(50, 50)))
            g.fitness = 0
            self.ge.append(g)

    def create_piping(self):
        gap_height = random.randrange(CANVAS_HEIGHT-600) + 200
        self.pipes.append(Pipe(Pos(CANVAS_WIDTH, gap_height-1000)))
        self.pipes.append(Pipe(Pos(CANVAS_WIDTH, gap_height + PIPE_GAP)))

    def check_collisions(self, bird):
        bird_bottom = bird.pos.y + bird.height
        bird_top = bird.pos.y
        bird_left = bird.pos.x
        bird_right = bird.pos.x + bird.width

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

        pipe_idx = 0
        if len(self.birds) > 0:
            if len(self.pipes) > 1 and self.birds[0].pos.x > self.pipes[0].pos.x + self.pipes[0].width:
                pipe_idx = 2
        else:
            self.lost = True

        closest_pipes = [self.pipes[pipe_idx], self.pipes[pipe_idx+1]]
        # Bird update
        for x, bird in enumerate(self.birds):
            output = self.nets[x].activate((bird.pos.y,
                                    bird.fly_speed, 
                                    abs(bird.pos.y - closest_pipes[0].height), 
                                    abs(bird.pos.y - closest_pipes[1].pos.y)))
            if output[0] > 0.5:
                bird.fly_up()

            bird.move()
            bird.draw(self.canvas)
            
            if bird.pos.y < 0:
                bird.pos.y = 0

            # Check Collisions
            if self.check_collisions(bird):
                self.ge[x].fitness -= 1
                self.birds.pop(x)
                self.ge.pop(x)
                self.nets.pop(x)
                self.canvas.delete(bird.canvas_obj)
            else:
                self.ge[x].fitness += 0.1

        # Produce pipes regularly
        self.counter += 1
        if self.counter % SCORE_FREQUENCY == 0:
            for g in self.ge:
                g.fitness += 5
            self.score += 1
            self.score_lbl_str.set(f"Score : {self.score}")
        if self.counter >= PIPE_FREQUENCY:
            self.counter = 0
            self.create_piping()

        # Update again
        if (not self.lost):
            self.canvas.after(CANVAS_UPDATE_SPEED, self.update)
        else:
            self.pack_forget()
            self.master.destroy()

gen = 0

def begin(genomes, config):
    global gen
    gen += 1
    print(f"Generation {gen}")
    root = Tk()
    root.title("Flappy Bird")
    app = flappy_bird(genomes, config, master=root)
    app.mainloop()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)

    p = neat.Population(config)
    winner = p.run(begin, 100)
    print('\nBest genome:\n{!s}'.format(winner)) 

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_config.txt")
    run(config_path)