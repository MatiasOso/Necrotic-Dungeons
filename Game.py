import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Cargar la imagen de fondo
background_image = pygame.image.load("bg.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Cargar la imagen del carrito de compra
cart_image = pygame.image.load("carrito.png")
cart_image = pygame.transform.scale(cart_image, (50, 50))
cart_rect = cart_image.get_rect()
cart_rect.bottomleft = (20, HEIGHT - 20)

# Colores en formato RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLATA = (192, 192, 192)

# Fuente del menú
font_path = "8bitwonder.ttf" 
font_size = 32

# Crear la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú Principal")

# Cargar la fuente
font = pygame.font.Font(font_path, font_size)

# Definir opciones del menú principal
menu_options = ["Iniciar sesion", "Registrarse", "Salir"]
selected_option = 0

# dinero y experiencia
money = 9999
XP = 9999

# Musica: https://www.youtube.com/watch?v=0ktyag1l3y8
# Musica : https://www.youtube.com/watch?v=QVfoZQ-0A1M
# Buscar como descargar musica de yotube quizas haga un porgrama que lo haga
# pygame.mixer.music.load("cancion.mp3")
# pygame.mixer.music.play(-1)  # Reproducir en bucle infinito

# Función para verificar si el cursor está sobre el carrito de compra
def is_cursor_on_cart():
    mouse_pos = pygame.mouse.get_pos()
    return cart_rect.collidepoint(mouse_pos)

# Variable para indicar si se encuentra en el menú de opciones
register = False

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not register:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        # Acción para la opción "Jugar"
                        print("¡Iniciar sesion!")
                    elif selected_option == 1:
                        # Abrir el menú de opciones
                        register = True
                        # pygame.mixer.music.pause()  
                    elif selected_option == 2:
                        # Acción para la opción "Salir"
                        running = False
                        sys.exit()
            else:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 2   #(registrarse y salir)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 2 
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        # Acción para la opción "Iniciar sesión"
                        print("Registrarse")
                    elif selected_option == 1:
                        # Acción para la opción "Volver"
                        register = False
                        pygame.mixer.music.unpause()  # Reanudar la reproducción de la canción

    # Dibujar la imagen de fondo
    window.blit(background_image, (0, 0))

    # Dibujar el carrito de compra
    if is_cursor_on_cart():
        enlarged_cart_image = pygame.transform.scale(cart_image, (60, 60))
        cart_rect.width = 60
        cart_rect.height = 60
        window.blit(enlarged_cart_image, cart_rect)
    else:
        window.blit(cart_image, cart_rect)

    # Renderizar las opciones del menú principal o del menú de opciones
    if not register:
        for i, option in enumerate(menu_options):
            text = font.render(option, True, WHITE if i == selected_option else PLATA)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * font_size))
            window.blit(text, text_rect)
    else:
        options_menu = ["Registrarse","Volver"]
        for i, option in enumerate(options_menu):
            text = font.render(option, True, WHITE if i == selected_option else PLATA)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * font_size))
            window.blit(text, text_rect)

    # Actualizar la pantalla
    pygame.display.flip()

# Cerrar Pygame al salir del juego
pygame.quit()
