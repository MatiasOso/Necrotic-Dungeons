import pygame
import sys
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLATA = (192, 192, 192)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Clase padre para los personajes
class Personaje:
    def __init__(self, salud, ataque, velocidad_movimiento, velocidad_ataque):
        self.salud = salud
        self.salud_maxima = salud
        self.ataque = ataque
        self.velocidad_movimiento = velocidad_movimiento
        self.velocidad_ataque = velocidad_ataque

    def ver_vida(self, ventana):
        pygame.draw.rect(ventana, ROJO, (self.x, self.y - 10, 64, 5))
        pygame.draw.rect(ventana, VERDE, (self.x, self.y - 10, 64 * (self.salud / self.salud_maxima), 5))

    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        if self.salud < 0:
            self.salud = 0

# Subclase para el personaje principal ("guy")
class Guy(Personaje):
    def __init__(self, x, y, imagen_izquierda, imagen_derecha):
        super().__init__(salud=100, ataque=10, velocidad_movimiento=5, velocidad_ataque=1)
        self.x = x
        self.y = y
        self.imagen_izquierda = imagen_izquierda
        self.imagen_derecha = imagen_derecha
        self.direccion = "izquierda"  # Inicialmente, mira hacia la izquierda

    def mover(self, direccion):
        if direccion == "izquierda":
            self.x -= self.velocidad_movimiento
            self.direccion = "izquierda"
        elif direccion == "derecha":
            self.x += self.velocidad_movimiento
            self.direccion = "derecha"

    def dibujar(self, ventana):
        if self.direccion == "izquierda":
            ventana.blit(self.imagen_izquierda, (self.x, self.y))
        else:
            ventana.blit(self.imagen_derecha, (self.x, self.y))

# Subclase para los enemigos
class Enemigo(Personaje):
    def __init__(self, x, y, imagen, velocidad):
        super().__init__(salud=50, ataque=5, velocidad_movimiento=velocidad, velocidad_ataque=0.5)
        self.x = x
        self.y = y
        self.imagen = imagen

    def mover(self, objetivo):
        dx = objetivo.x - self.x
        dy = objetivo.y - self.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia > 0:
            dx_norm = dx / distancia
            dy_norm = dy / distancia
            self.x += dx_norm * self.velocidad_movimiento
            self.y += dy_norm * self.velocidad_movimiento

    def dibujar(self, ventana):
        ventana.blit(self.imagen, (self.x, self.y))

# Crear instancias de los personajes
guy_izquierda = pygame.image.load("./imagenes/guy.png")
guy_izquierda = pygame.transform.scale(guy_izquierda, (64, 64))
guy_derecha = pygame.transform.flip(guy_izquierda, True, False)

guy = Guy(x=WIDTH // 2, y=HEIGHT // 2, imagen_izquierda=guy_izquierda, imagen_derecha=guy_derecha)

enemigo_imagen = pygame.image.load("./imagenes/guy.png")
enemigo_imagen = pygame.transform.scale(enemigo_imagen, (64, 64))
enemigo = Enemigo(x=100, y=100, imagen=enemigo_imagen, velocidad=2)

# Fondo
fondo = pygame.image.load("./imagenes/floor.png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

# Configuración de la fuente
font_path = "8bitwonder.ttf"
font_size = 32
font = pygame.font.Font(font_path, font_size)

# Inicializar la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego")

clock = pygame.time.Clock()

while True:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del personaje principal
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        guy.mover("izquierda")
    if keys[pygame.K_RIGHT]:
        guy.mover("derecha")
    if keys[pygame.K_UP]:
        guy.y -= guy.velocidad_movimiento
    if keys[pygame.K_DOWN]:
        guy.y += guy.velocidad_movimiento

    # Movimiento del enemigo
    enemigo.mover(guy)

    # Colisión del enemigo con el personaje principal
    if math.sqrt((guy.x - enemigo.x) ** 2 + (guy.y - enemigo.y) ** 2) < 32:
        guy.recibir_dano(enemigo.ataque)

    # Dibujar en la ventana
    window.blit(fondo, (0, 0))
    guy.dibujar(window)
    guy.ver_vida(window)
    enemigo.dibujar(window)
    enemigo.ver_vida(window)

    pygame.display.flip()
    clock.tick(60)
