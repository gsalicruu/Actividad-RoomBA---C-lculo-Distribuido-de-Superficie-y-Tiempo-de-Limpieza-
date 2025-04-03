import pygame
from config import GRID_SIZE

def update_pelusas(pelusas, roomba_pos, bullets):
    new_pelusas = []
    for pelusa in pelusas:
        pelusa_rect = pygame.Rect(pelusa[0], pelusa[1], GRID_SIZE, GRID_SIZE)
        hit = False
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)
            if pelusa_rect.colliderect(bullet_rect):
                bullet.active = False
                hit = True
                break
        if not hit and pelusa != roomba_pos:
            new_pelusas.append(pelusa)
    return new_pelusas

