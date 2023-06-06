import pygame
import sys


pygame.init()

WIDTH = 800
HEIGHT = 600

background_image = pygame.image.load("bg.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

#weas del carro
cart_image = pygame.image.load("carrito.png")
cart_image = pygame.transform.scale(cart_image, (50, 50))
cart_rect = cart_image.get_rect()
cart_rect.bottomleft = (20, HEIGHT - 20)

# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
GOLDEN = (255, 215, 0)
# Fuente del menú
font_path = "8bitwonder.ttf"  # Ruta de la fuente 8-bit (puedes descargarla de Internet)
font_size = 32

# Crear la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú Principal")

# Cargar la fuente
font = pygame.font.Font(font_path, font_size)

# Definir opciones del menú principal
menu_options = ["Jugar", "Opciones", "Tutorial", "Salir"]
selected_option = 0

# Definir opciones del menú de opciones
options_menu_options = ["Iniciar sesión", "Volumen", "Volver"]
selected_options_menu_option = 0

# Definir variables de dinero y experiencia
money = 9999
XP = 9999

# Variable para controlar la reproducción de música
music_playing = False

# Cargar la canción
# Musica: https://www.youtube.com/watch?v=0ktyag1l3y8
# Musica : https://www.youtube.com/watch?v=QVfoZQ-0A1M
# pygame.mixer.music.load("cancion.mp3")

# Función para verificar si el cursor está sobre el carrito de compra
def is_cursor_on_cart():
    mouse_pos = pygame.mouse.get_pos()
    return cart_rect.collidepoint(mouse_pos)

# Bucle principal del juego
running = True
in_options_menu = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not in_options_menu:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        # Acción para la opción "Jugar"
                        print("¡Iniciar juego!")
                    elif selected_option == 1:
                        # Abrir el menú de opciones
                        in_options_menu = True
                        pygame.mixer.music.pause()
                    elif selected_option == 2:
                        # Acción para la opción "Tutorial"
                        print("¡Abrir tutorial!")
                    elif selected_option == 3:
                        # Acción para la opción "Salir"
                        running = False
                        sys.exit()
            else:
                if event.key == pygame.K_UP:
                    selected_options_menu_option = (selected_options_menu_option - 1) % len(options_menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_options_menu_option = (selected_options_menu_option + 1) % len(options_menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_options_menu_option == 0:
                        # Acción para la opción "Iniciar sesión"
                        print("¡Iniciar sesión!")
                    elif selected_options_menu_option == 1:
                        # Acción para la opción "Volumen"
                        if music_playing:
                            pygame.mixer.music.stop()
                            music_playing = False
                        else:
                            pygame.mixer.music.play(-1)
                            music_playing = True
                    elif selected_options_menu_option == 2:
                        # Acción para la opción "Volver"
                        in_options_menu = False
                        pygame.mixer.music.unpause()

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

    if not in_options_menu:
        # Renderizar las opciones del menú principal
        for i, option in enumerate(menu_options):
            text = font.render(option, True, WHITE if i == selected_option else SILVER)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * font_size))
            window.blit(text, text_rect)
    else:
        # Renderizar las opciones del menú de opciones
        for i, option in enumerate(options_menu_options):
            text = font.render(option, True, WHITE if i == selected_options_menu_option else SILVER)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * font_size))
            window.blit(text, text_rect)

    # Actualizar la pantalla
    pygame.display.flip()

# Cerrar Pygame al salir del juego
pygame.quit()
