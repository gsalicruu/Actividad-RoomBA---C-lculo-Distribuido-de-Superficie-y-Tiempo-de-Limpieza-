import pygame
from config import GRID_SIZE
from tcp_client import notificar_limpieza

def update_pelusas(pelusas, roomba_pos, bullets):
    new_pelusas = []
    roomba_rect = pygame.Rect(roomba_pos[0], roomba_pos[1], GRID_SIZE, GRID_SIZE)

    for pelusa in pelusas:
        pelusa_rect = pygame.Rect(pelusa[0], pelusa[1], GRID_SIZE, GRID_SIZE)
        hit = False

        # Colisión con balas
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)
            if pelusa_rect.colliderect(bullet_rect):
                bullet.active = False
                if notificar_limpieza(pelusa[0], pelusa[1]):
                    hit = True
                break

        # Colisión con la Roomba
        if not hit and pelusa_rect.colliderect(roomba_rect):
            if notificar_limpieza(pelusa[0], pelusa[1]):
                hit = True

        # Si no fue eliminada, se mantiene
        if not hit:
            new_pelusas.append(pelusa)

    return new_pelusas
