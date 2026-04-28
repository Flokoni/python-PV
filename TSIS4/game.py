import pygame, random
from config import *

class Snake:
    def __init__(self, color):
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.dir = [CELL, 0]
        self.color = color
        self.shield = False

    def move(self, grow=True):
        head = [self.body[0][0] + self.dir[0], self.body[0][1] + self.dir[1]]
        self.body.insert(0, head)
        if not grow: self.body.pop()

class Food:
    def __init__(self, snake_body, walls, f_type="normal"):
        self.type = f_type 
        self.colors = {"normal": GREEN, "poison": (100, 0, 0), "speed": YELLOW, "slow": BLUE, "shield": PURPLE}
        self.spawn(snake_body, walls)
        self.spawn_time = pygame.time.get_ticks()

    def spawn(self, snake_body, walls):
        while True:
            self.pos = [random.randrange(0, WIDTH//CELL)*CELL, random.randrange(0, HEIGHT//CELL)*CELL]
            if self.pos not in snake_body and self.pos not in walls: break

class Obstacle:
    def __init__(self, level, snake_body):
        self.blocks = []
        if level >= 3:
            for _ in range(level * 2):
                while True:
                    b = [random.randrange(0, WIDTH//CELL)*CELL, random.randrange(0, HEIGHT//CELL)*CELL]
                    
                    if b not in snake_body and abs(b[0]-snake_body[0][0]) > CELL*2:
                        self.blocks.append(b)
                        break