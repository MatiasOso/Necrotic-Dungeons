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
GOLDEN = (255, 215, 0)

# Variables de tiempo
tiempo = 0
tiempo_inicio = pygame.time.get_ticks()

# Cooldown del disparo
ultimo_disparo_tiempo = 0


# Clase padre para los personajes
class Personaje:
    def __init__(self, salud, ataque, velocidad_movimiento, velocidad_ataque):
        self.salud = salud
        self.salud_maxima = salud
        self.ataque = ataque
        self.velocidad_movimiento = velocidad_movimiento
        self.velocidad_ataque = velocidad_ataque
        self.balas = []

    def ver_vida(self, ventana):
        pygame.draw.rect(ventana, ROJO, (self.x, self.y - 10, 64, 5))
        pygame.draw.rect(ventana, VERDE, (self.x, self.y - 10, 64 * (self.salud / self.salud_maxima), 5))

    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        if self.salud < 0:
            self.salud = 0

    def disparar(self, objetivo):
        dx = objetivo.x - self.x
        dy = objetivo.y - self.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia > 0:
            dx_norm = dx / distancia
            dy_norm = dy / distancia
            bala = Bala(self.x, self.y, dx_norm, dy_norm)
            self.balas.append(bala)

    def mover_balas(self):
        for bala in self.balas:
            bala.mover()
            if bala.x < 0 or bala.x > WIDTH or bala.y < 0 or bala.y > HEIGHT:
                self.balas.remove(bala)

    def dibujar_balas(self, ventana):
        for bala in self.balas:
            bala.dibujar(ventana)

# Subclase para el personaje principal ("guy")
class Guy(Personaje):
    def __init__(self, x, y, imagen_izquierda, imagen_derecha):
        super().__init__(salud=300, ataque=10, velocidad_movimiento=5, velocidad_ataque=1)
        self.x = x
        self.y = y
        self.imagen_izquierda = imagen_izquierda
        self.imagen_derecha = imagen_derecha
        self.direccion = "izquierda"  # Inicialmente, mira hacia la izquierda

    def mover(self, direccion):
        if direccion == "izquierda" and self.x > 0:
            self.x -= self.velocidad_movimiento
            self.direccion = "izquierda"
        elif direccion == "derecha" and self.x < WIDTH - 64:
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
        super().__init__(salud=300, ataque=5, velocidad_movimiento=velocidad, velocidad_ataque=0.5)
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

# Clase para las balas
class Bala:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.velocidad = 10

    def mover(self):
        self.x += self.dx * self.velocidad
        self.y += self.dy * self.velocidad

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, GOLDEN, (self.x, self.y, 10, 5))

# Crear instancias de los personajes
guy_izquierda = pygame.image.load("./imagenes/guy.png")
guy_izquierda = pygame.transform.scale(guy_izquierda, (64, 64))
guy_derecha = pygame.transform.flip(guy_izquierda, True, False)

# Instancia del personaje principal
guy = Guy(x=WIDTH // 2, y=HEIGHT // 2, imagen_izquierda=guy_izquierda, imagen_derecha=guy_derecha)

# Instancia del enemigo
enemigo_imagen = pygame.image.load("./imagenes/guy.png")
enemigo_imagen = pygame.transform.scale(enemigo_imagen, (64, 64))
enemigo = Enemigo(x=100, y=100, imagen=enemigo_imagen, velocidad=2)

# Fondo
fondo = pygame.image.load("./imagenes/piso.png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
fondo_x = 0
fondo_y = 0

# Configuración de la fuente
font_path = "8bitwonder.ttf"
font_size = 32
font = pygame.font.Font(font_path, font_size)




# Inicializar la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego")

clock = pygame.time.Clock()

color = WHITE

while True:
    # Actualizar temporizador
    tiempo = (pygame.time.get_ticks() - tiempo_inicio) // 100

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Movimiento del personaje principal
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        guy.mover("izquierda")
        fondo_x += 5
    if keys[pygame.K_RIGHT]:
        guy.mover("derecha")
        fondo_x -= 5
    if keys[pygame.K_UP]:
        guy.y -= guy.velocidad_movimiento
        fondo_y += 5
    if keys[pygame.K_DOWN]:
        guy.y += guy.velocidad_movimiento
        fondo_y -= 5
    if keys[pygame.K_SPACE] and pygame.time.get_ticks() - ultimo_disparo_tiempo >= 500:  # Intervalo mínimo de 500 milisegundos entre disparos
        guy.disparar(enemigo)
        ultimo_disparo_tiempo = pygame.time.get_ticks()


    # Limitar el movimiento del personaje dentro de la pantalla
    guy.x = max(0, min(guy.x, WIDTH - 64))
    guy.y = max(0, min(guy.y, HEIGHT - 64))

    # Movimiento del enemigo
    enemigo.mover(guy)

    # Colisión del enemigo con el personaje principal
    if math.sqrt((guy.x - enemigo.x) ** 2 + (guy.y - enemigo.y) ** 2) < 32:
        guy.recibir_dano(enemigo.ataque)

    # Movimiento de las balas
    guy.mover_balas()

    if int(tiempo) % 7 == 0:
        color = ROJO
    else:
        color = WHITE


    # Colisión de las balas con el enemigo
    for bala in guy.balas:
        if math.sqrt((bala.x - enemigo.x) ** 2 + (bala.y - enemigo.y) ** 2) < 32:
            enemigo.recibir_dano(guy.ataque)
            guy.balas.remove(bala)

    # Dibujar en la ventana
        # Dibujar en la ventana
    for x in range(fondo_x % WIDTH - WIDTH, WIDTH, WIDTH):
        for y in range(fondo_y % HEIGHT - HEIGHT, HEIGHT, HEIGHT):
            window.blit(fondo, (x, y))
    tiempo_texto = font.render("Time " + str(tiempo), True, color)
    window.blit(tiempo_texto, (300, 10))
    guy.dibujar(window)
    guy.ver_vida(window)
    enemigo.dibujar(window)
    enemigo.ver_vida(window)
    guy.dibujar_balas(window)

    pygame.display.flip()
    clock.tick(60)
# HASTA AQUI VA BIEN