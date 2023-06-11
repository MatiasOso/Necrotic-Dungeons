import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Colores en formato RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLATA = (192, 192, 192)

# Fuente del menú
font_path = "8bitwonder.ttf"  # Ruta de la fuente 8-bit (puedes descargarla de Internet)
font_size = 32

# Sonidos
def play_change_sound():
    pygame.mixer.music.load("cambio.wav")
    pygame.mixer.music.play(0)



# Crear la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú Principal")

# Cargar la fuente
font = pygame.font.Font(font_path, font_size)

# fondo
background_image = pygame.image.load("bg.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
#opciones del menú
menu_options = ["Jugar", "Opciones", "Salir"]
selected_option = 0

# Bucle principal del juego
# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
                play_change_sound()
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
                play_change_sound()
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    # Dejar la ventana en negro
                    window.fill(BLACK)  # Llenar la ventana con color negro
                    pygame.display.flip()  # Actualizar la pantalla
                    print("¡Iniciar juego!")
                elif selected_option == 1:
                    # Acción para la opción "Opciones"
                    print("Abrir opciones")
                elif selected_option == 2:
                    # Acción para la opción "Salir"
                    running = False
                    sys.exit()
    
    # Dibujar la imagen de fondo
    window.blit(background_image, (0, 0))
    
    # Renderizar las opciones del menú
    for i, option in enumerate(menu_options):
        text = font.render(option, True, WHITE if i == selected_option else PLATA)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * font_size))
        window.blit(text, text_rect)
    
    # Actualizar la pantalla
    pygame.display.flip()

# Cerrar Pygame al salir del juego
pygame.quit()


