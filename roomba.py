import pygame
import math
import time
from config import GRID_SIZE, BLUE, SHOOT_DELAY
from bullet import Bullet

class Roomba:
    def __init__(self, start_pos):
        self.x, self.y = start_pos
        self.speed = GRID_SIZE
        self.angle = 0
        self.last_shot_time = 0

    def move(self, dx, dy):
        if dx != 0 or dy != 0:
            self.angle = math.atan2(dy, dx)
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(0, min(self.x, 800 - GRID_SIZE))
        self.y = max(0, min(self.y, 600 - GRID_SIZE))

    def can_shoot(self):
        return time.time() - self.last_shot_time >= SHOOT_DELAY

    def shoot(self):
        if self.can_shoot():
            self.last_shot_time = time.time()
            return Bullet(self.x, self.y, self.angle)
        return None

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 2)
