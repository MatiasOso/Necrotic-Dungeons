import pygame
import sys
import tkinter as tk

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import tkinter as tk
# Para ejecutar el juego de verdad
import subprocess



uri = "mongodb+srv://matiasosores:XJLMzLTVcFYc7iCt@tienda.ietwuqs.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
def conexion():
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Conexión exitosa")
        db = client.test
        return db
    except Exception as e:
        print(e)

db = conexion()



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
 #Nickname,correo,contraseña, confirmar contraseña
# dinero y experiencia
money = 9999
XP = 9999

#Debo crear la clase raza esta debe tener atributos como, nombre (de la raza), descripcion, imagen, HP, daño de ataque, velocidad
# Y NO SÉ COMO BUSCO TUTORIAL NO HAY NADA AYUDA!!!!
running = True
def iniciar_sesion():
    # Función para guardar los datos en la base de datos
    def check_datos():
        global label5  # Declarar label5 como variable global
        Nickname = entry1.get()
        Contraseña = entry2.get()

        documentos = {
            "Nickname": Nickname,
            "Contraseña": Contraseña
        }
        login = False
        if Nickname == 'admin' and Contraseña == 'admin':
            # Abrir el programa admin.py
            subprocess.Popen(["python", "admin.py"])
        elif db.Usuarios.find_one(documentos):
            print("Inicio de sesión exitoso")
            label5 = tk.Label(ventana, text="Inicio de sesión exitoso")
            label5.grid(row=5, column=1)
            boton.config(state=tk.DISABLED)
            ventana.after(1000, ocultar_mensaje)
            ventana.after(2000, ventana.destroy)
            # validar el login
            subprocess.Popen(["python", "experimento.py"])
            login = True
            # Destruir esta ventana
            ventana.destroy()
        else:
            print("Inicio de sesión fallido")
            label5 = tk.Label(ventana, text="Error de contraseña o usuario")
            label5.grid(row=5, column=1)
            boton.config(state=tk.DISABLED)
            ventana.after(1000, ocultar_mensaje)
            ventana.after(2000, ventana.destroy)


    # Función para ocultar el mensaje
    def ocultar_mensaje():
        label5.grid_remove()

    # Crear una ventana
    ventana = tk.Tk()
    ventana.title("Iniciar sesión")
    ventana.geometry("400x150")

    # Crear los labels
    label1 = tk.Label(ventana, text="Nickname")
    label1.grid(row=0, column=0)
    label2 = tk.Label(ventana, text="Contraseña")
    label2.grid(row=1, column=0)

    # Crear los entrys
    entry1 = tk.Entry(ventana)
    entry1.grid(row=0, column=1)
    entry2 = tk.Entry(ventana, show="*")
    entry2.grid(row=1, column=1)

    # Crear el botón de registro
    boton = tk.Button(ventana, text="Iniciar sesión", command=check_datos)
    boton.grid(row=4, column=1)
    ventana.mainloop()

# Musica: https://www.youtube.com/watch?v=0ktyag1l3y8
# Musica : https://www.youtube.com/watch?v=QVfoZQ-0A1M
# Buscar como descargar musica de yotube quizas haga un porgrama que lo haga
# pygame.mixer.music.load("totusflo.mp3")
# pygame.mixer.music.play(-1)   Reproducir en bucle infinito

# Función para verificar si el cursor está sobre el carrito de compra
def is_cursor_on_cart():
    mouse_pos = pygame.mouse.get_pos()
    return cart_rect.collidepoint(mouse_pos)

# Variable para indicar si se encuentra en el menú de opciones
register = False

# Funcion para reproducir cambio.wav cada vez que cambie de opción
def play_change_sound():
    pygame.mixer.music.load("cambio.wav")
    pygame.mixer.music.play(0)

# ------------------------------------------------- JUEGO ------------------------------------------------- #
# ------------------------------------------------- JUEGO ------------------------------------------------- #
# ------------------------------------------------- JUEGO ------------------------------------------------- #
# ------------------------------------------------- JUEGO ------------------------------------------------- #

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not register:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_option = (selected_option - 1) % len(menu_options)
                    play_change_sound()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % len(menu_options)
                    play_change_sound()
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        iniciar_sesion()
                        print("¡Iniciar sesion!")
                    elif selected_option == 1:
                        # Abrir el menú de opciones
                        register = True 
                    elif selected_option == 2:
                        # Acción para la opción "Salir"
                        running = False
                        sys.exit()
            else:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_option = (selected_option - 1) % 2   #(registrarse y salir)
                    play_change_sound()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % 2 
                    play_change_sound()
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        # Registro pide Nickname, correo, contraseña, confirmar contraseña
                        def registro():
                            # Función para guardar los datos en la base de datos
                            def guardar_datos():
                                global label5  # Declarar label5 como variable global
                                nickname = entry1.get()
                                correo = entry2.get()
                                contraseña = entry3.get()
                                confirmar_contraseña = entry4.get()

                                if contraseña == confirmar_contraseña:
                                    documentos = {
                                        "Nickname": nickname,
                                        "Correo": correo,
                                        "Contraseña": contraseña,
                                        "Confirmar contraseña": confirmar_contraseña,
                                        "es_gm": False
                                    }
                                    for documento in db.Usuarios.find():
                                        if nickname == documento["Nickname"]:
                                            print("El nickname ya existe")
                                            label5 = tk.Label(ventana, text="El nickname ya existe")
                                            label5.grid(row=5, column=1)
                                            ventana.after(1000, ocultar_mensaje)
                                            return
                                        else:
                                            db.Usuarios.insert_one(documentos)
                                            label5 = tk.Label(ventana, text="Registro exitoso")
                                            label5.grid(row=5, column=1)
                                            boton.config(state=tk.DISABLED)
                                            ventana.after(1000, ocultar_mensaje)
                                            ventana.after(2000, ventana.destroy)  

                                else:
                                    print("Las contraseñas no coinciden")
                                    label5 = tk.Label(ventana, text="Las contraseñas no coinciden")
                                    label5.grid(row=5, column=1)
                                    ventana.after(1000, ocultar_mensaje)  

                            # Función para ocultar el mensaje
                            def ocultar_mensaje():
                                label5.grid_remove()

                            # Crear una ventana
                            ventana = tk.Tk()
                            ventana.title("Registro")
                            ventana.geometry("400x200")

                            # Crear los labels
                            label1 = tk.Label(ventana, text="Nickname")
                            label1.grid(row=0, column=0)
                            label2 = tk.Label(ventana, text="Correo")
                            label2.grid(row=1, column=0)
                            label3 = tk.Label(ventana, text="Contraseña")
                            label3.grid(row=2, column=0)
                            label3 = tk.Label(ventana, text="RepitaContraseña")
                            label3.grid(row=3, column=0)
                            # Crear los entrys
                            entry1 = tk.Entry(ventana)
                            entry1.grid(row=0, column=1)
                            entry2 = tk.Entry(ventana)
                            entry2.grid(row=1, column=1)
                            entry3 = tk.Entry(ventana, show="*")
                            entry3.grid(row=2, column=1)
                            entry4 = tk.Entry(ventana, show="*")
                            entry4.grid(row=3, column=1)

                            # Crear el botón de registro
                            boton = tk.Button(ventana, text="Registrarse", command=guardar_datos)
                            boton.grid(row=4, column=1)

                            ventana.mainloop()

                        registro()

                        print("Registrarse")
                    elif selected_option == 1:
                        # Acción para la opción "Volver"
                        register = False
                          # Reanudar la reproducción de la canción

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


# --------------------ADMIN EVENTS ----------------------------- # Esto quizas deberia ir más arriba ¯\_(ツ)_/¯