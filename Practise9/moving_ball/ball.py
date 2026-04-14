import pygame

class Ball:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.radius = 25
        self.color = (255, 0, 0) 
        self.step = 20 
        
        self.x = screen_width // 2
        self.y = screen_height // 2

    def move(self, direction):
        if direction == "UP":
            if self.y - self.step >= self.radius:
                self.y -= self.step
        elif direction == "DOWN":
            if self.y + self.step <= self.screen_height - self.radius:
                self.y += self.step
        elif direction == "LEFT":
            if self.x - self.step >= self.radius:
                self.x -= self.step
        elif direction == "RIGHT":
            if self.x + self.step <= self.screen_width - self.radius:
                self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)