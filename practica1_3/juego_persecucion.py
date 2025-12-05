import pygame
import sys
import math
import csv
import os
from datetime import datetime

# --- 1. Inicialización de Pygame y Constantes ---
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Evasión con Persecución")

# Colores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)      # Color para el Sensor (Jugador)
BLUE = (0, 0, 255)     # Color para el Perseguidor (Lejos)
GREEN = (0, 255, 0)    # Color para el Perseguidor (Cerca)

# Otros objetos de Pygame
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# --- 2. Clases de Objetos ---
class Sensor:
    """Objeto controlado por el usuario (el que evade)."""
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 30, 30) # Posición inicial y tamaño
        self.speed = 5
        self.trail = [] # Para dibujar el rastro de movimiento

    def draw(self):
        # Dibuja el objeto principal
        pygame.draw.rect(screen, RED, self.rect)
        # Dibuja el rastro de los últimos 20 puntos
        for pos in self.trail[-20:]:
            pygame.draw.circle(screen, (255, 100, 100), pos, 2)
    
    def move(self, keys):
        # Guarda la posición actual antes de mover
        old_pos = (self.rect.centerx, self.rect.centery)
        
        # Lógica de movimiento y límites de la pantalla
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
        # Guarda la nueva posición en el rastro si hubo movimiento
        new_pos = (self.rect.centerx, self.rect.centery)
        if new_pos != old_pos:
            self.trail.append(new_pos)

class ObjetoPerseguidor:
    """Objeto que sigue al Sensor."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30) # Posición inicial y tamaño
        self.speed = 2 # Velocidad de persecución
        self.color = BLUE
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def move(self, target_pos):
        target_x, target_y = target_pos
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        
        # Calcula la distancia euclidiana
        distance = math.sqrt(dx**2 + dy**2)
        
        # Evita la división por cero si están exactamente en el mismo lugar
        if distance > 0:
            # Normaliza el vector (dx, dy) y lo multiplica por la velocidad
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed
        
        # Cambia de color si está cerca (radio < 100)
        self.color = GREEN if distance < 100 else BLUE

# --- 3. Inicialización del Juego y CSV ---
# Crear el sensor y dos objetos perseguidores
sensor = Sensor()
objetos = [
    ObjetoPerseguidor(WIDTH - 100, HEIGHT - 100),
    ObjetoPerseguidor(WIDTH // 2, 50)
]

# Configuración del archivo CSV para el registro de datos
csv_file = "datos_persecucion.csv"
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    # Encabezados del archivo
    writer.writerow(['Timestamp', 'Player_X', 'Player_Y', 'Obj1_X', 'Obj1_Y',
                     'Obj2_X', 'Obj2_Y'])

# --- 4. Bucle Principal del Juego ---
running = True
while running:
    # 1. Manejo de Eventos (Cerrar la ventana)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 2. Lógica del Juego
    keys = pygame.key.get_pressed()
    sensor.move(keys) # Mover el jugador/sensor
    
    # Mover a los perseguidores hacia el centro del sensor
    for obj in objetos:
        obj.move(sensor.rect.center)
    
    # 3. Registro de Datos (Se registra cada 5 ciclos de reloj)
    if pygame.time.get_ticks() % 5 == 0:
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%H:%M:%S.%f"),
                sensor.rect.centerx,
                sensor.rect.centery,
                objetos[0].rect.centerx,
                objetos[0].rect.centery,
                objetos[1].rect.centerx,
                objetos[1].rect.centery
            ])
    
    # 4. Dibujo
    screen.fill(BLACK) # Limpiar la pantalla
    sensor.draw()
    for obj in objetos:
        obj.draw()
    
    # Mostrar texto de ayuda
    text = font.render("Usa las flechas en tu teclado para moverte. Objetos te persiguen!", True, WHITE)
    screen.blit(text, (10, 10))
    
    # 5. Actualizar la Pantalla y Controlar FPS
    pygame.display.flip()
    clock.tick(60) # Limita el juego a 60 fotogramas por segundo

# --- 5. Salida ---
pygame.quit()
sys.exit()