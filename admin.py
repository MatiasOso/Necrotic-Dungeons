import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import tkinter as tk
# from Game.py import db


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
# Open window for CRUD operations

def ventana():
    # Create window

    ventana = tk.Tk()
    ventana.title("CRUD")
    ventana.geometry("400x150")

    
    # Create user
    boton = tk.Button(ventana, text="Crear GameMaster")
    boton.grid(row=0, column=0, padx=3, pady=50)
    # Abrir formulario para crear usuario
    # Debe llenar n formulario con los datos del usuario los cuales son Nickname, email, contraseña, es_gm(debe ser true or false)
    
   
    
    # Read user
    boton = tk.Button(ventana, text="Leer usuarios")
    boton.grid(row=0, column=1, padx=3, pady=50)
    
    # Update user
    boton = tk.Button(ventana, text="Actualizar usuario") #Posibles baneos o desbaneos y/o suspensiones
    boton.grid(row=0, column=2, padx=3, pady=50)
    # Delete user
    boton = tk.Button(ventana, text="Borrar usuario")
    boton.grid(row=0, column=3, padx=3, pady=50)
    ventana.mainloop()
ventana()