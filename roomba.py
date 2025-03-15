import pygame
import random
import math
import time
import concurrent.futures

# Configuración inicial
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
NUM_PELUSAS = 10
BULLET_SPEED = 10
SHOOT_DELAY = 2  # Tiempo entre disparos en segundos

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roomba Cleaner")
clock = pygame.time.Clock()

# Variables globales para concurrencia
roomba_pos = None
pelusas = []

# Clase Roomba
class Roomba:
    def __init__(self, start_pos):
        self.x, self.y = start_pos
        self.speed = GRID_SIZE
        self.angle = 0  # Ángulo de dirección
        self.last_shot_time = 0

    def move(self, dx, dy):
        if dx != 0 or dy != 0:
            self.angle = math.atan2(dy, dx)
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(0, min(self.x, WIDTH - GRID_SIZE))
        self.y = max(0, min(self.y, HEIGHT - GRID_SIZE))

    def can_shoot(self):
        return time.time() - self.last_shot_time >= SHOOT_DELAY

    def shoot(self):
        if self.can_shoot():
            self.last_shot_time = time.time()
            return Bullet(self.x, self.y, self.angle)
        return None

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 2)

# Clase Bullet
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

    def draw(self):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 5)

# Función para generar la posición inicial de la Roomba
def spawn_roomba():
    print("[Task] Creando Roomba...")
    return (random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE, 
            random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

# Función para generar pelusas aleatorias
def spawn_pelusas():
    print("[Task] Creando pelusas...")
    return [(random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE, 
             random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE) for _ in range(NUM_PELUSAS)]

# Función para actualizar la lista de pelusas
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

# Función principal
def main():
    global roomba_pos, pelusas
    
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
            bullet.draw()
        
        roomba.draw()
        pygame.display.flip()
        clock.tick(30)
        
        if not pelusas:
            print("¡Has limpiado todas las pelusas! Juego terminado.")
            running = False
    
    pygame.quit()
    print("[Main] Juego terminado.")

if __name__ == "__main__":
    main()
