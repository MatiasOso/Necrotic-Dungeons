from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import tkinter as tk

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
