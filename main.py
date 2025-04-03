import pygame
import random
import concurrent.futures
from roomba import Roomba
from pelusa import update_pelusas
from bullet import Bullet
from config import WIDTH, HEIGHT, WHITE, RED, GRID_SIZE, NUM_PELUSAS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roomba Cleaner")
clock = pygame.time.Clock()

# Función para generar la posición inicial de la Roomba
def spawn_roomba():
    print("[Task] Creando Roomba...")
    return (
        random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
        random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE
    )

# Función para generar pelusas aleatorias
def spawn_pelusas():
    print("[Task] Creando pelusas...")
    return [
        (
            random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
            random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        ) for _ in range(NUM_PELUSAS)
    ]

# Función principal
def main():
    print("[Main] Iniciando tareas...")
    tasks = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks[executor.submit(spawn_roomba)] = "Spawn de Roomba"
        tasks[executor.submit(spawn_pelusas)] = "Spawn de Pelusas"

        for future in concurrent.futures.as_completed(tasks):
            task_name = tasks[future]
            try:
                result = future.result()
            except Exception as exc:
                print(f"[Error] La tarea {task_name} generó una excepción: {exc}")
            else:
                if task_name == "Spawn de Roomba":
                    roomba_pos = result
                elif task_name == "Spawn de Pelusas":
                    pelusas = result
                print(f"[Main] {task_name} completada.")

    print("[Main] Todas las tareas han finalizado.")

    roomba = Roomba(roomba_pos)
    bullets = []

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullet = roomba.shoot()
                if bullet:
                    bullets.append(bullet)

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy = -1
        if keys[pygame.K_s]: dy = 1
        if keys[pygame.K_a]: dx = -1
        if keys[pygame.K_d]: dx = 1

        roomba.move(dx, dy)
        pelusas = update_pelusas(pelusas, (roomba.x, roomba.y), bullets)

        for bullet in bullets:
            bullet.move()
        bullets = [bullet for bullet in bullets if bullet.active]

        for pelusa in pelusas:
            pygame.draw.circle(screen, RED, (pelusa[0] + GRID_SIZE // 2, pelusa[1] + GRID_SIZE // 2), GRID_SIZE // 2)

        for bullet in bullets:
            bullet.draw(screen)

        roomba.draw(screen)
        pygame.display.flip()
        clock.tick(30)

        if not pelusas:
            print("¡Has limpiado todas las pelusas! Juego terminado.")
            running = False

    pygame.quit()
    print("[Main] Juego terminado.")

if __name__ == "__main__":
    main()
