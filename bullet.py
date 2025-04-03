import pygame
import math
from config import BULLET_SPEED, GRID_SIZE, GREEN, WIDTH, HEIGHT

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x + GRID_SIZE // 2
        self.y = y + GRID_SIZE // 2
        self.angle = angle
        self.speed = BULLET_SPEED
        self.active = True

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.active = False

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 5)
