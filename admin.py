import tkinter as tk
from tkinter import messagebox

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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

def guardar_datos():
    nickname = entry1.get()
    correo = entry2.get()
    contrasena = entry3.get()
    confirmar_contrasena = entry4.get()
    gm = gm_var.get()

    # Aquí puedes realizar las validaciones necesarias antes de guardar los datos

    # Guardar los datos en la base de datos
    # ...

    messagebox.showinfo("Éxito", "Los datos se guardaron correctamente")

def leer_usuarios():
    # Obtener la colección de usuarios
    usuarios_collection = db['Usuarios']
    
    # Obtener todos los documentos de la colección
    usuarios = usuarios_collection.find()
    
    # Crear una ventana emergente para mostrar los usuarios
    ventana_usuarios = tk.Toplevel()
    ventana_usuarios.title("Usuarios")
    
    # Crear un Text widget para mostrar los usuarios
    usuarios_text = tk.Text(ventana_usuarios)
    usuarios_text.pack()
    
    # Mostrar cada usuario en el Text widget
    for usuario in usuarios:
        usuarios_text.insert(tk.END, f"Nickname: {usuario['Nickname']}\n")
        usuarios_text.insert(tk.END, f"Correo: {usuario['Correo']}\n")
        usuarios_text.insert(tk.END, f"Contraseña: {usuario['Contraseña']}\n")
        usuarios_text.insert(tk.END, f"GM: {usuario['es_gm']}\n")
        usuarios_text.insert(tk.END, "\n")
    
    # Desactivar la edición en el Text widget
    usuarios_text.configure(state="disabled")

def ventana():
    ventana = tk.Tk()
    ventana.title("CRUD")
    ventana.geometry("400x150")

    boton_crear = tk.Button(ventana, text="Crear GameMaster", command=ventana_registro)
    boton_crear.grid(row=0, column=0, padx=3, pady=50)

    boton_leer = tk.Button(ventana, text="Leer usuarios", command=leer_usuarios)
    boton_leer.grid(row=0, column=1, padx=3, pady=50)

    # boton_actualizar = tk.Button(ventana, text="Actualizar usuario")
    # boton_actualizar.grid(row=0, column=2, padx=3, pady=50)

    # boton_borrar = tk.Button(ventana, text="Borrar usuario")
    # boton_borrar.grid(row=0, column=3, padx=3, pady=50)

    ventana.mainloop()

def ventana_registro():
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro")
    ventana_registro.geometry("400x200")

    label1 = tk.Label(ventana_registro, text="Nickname")
    label1.grid(row=0, column=0)
    label2 = tk.Label(ventana_registro, text="Correo")
    label2.grid(row=1, column=0)
    label3 = tk.Label(ventana_registro, text="Contraseña")
    label3.grid(row=2, column=0)
    label4 = tk.Label(ventana_registro, text="Confirmar Contraseña")
    label4.grid(row=3, column=0)
    label5 = tk.Label(ventana_registro, text="GM")
    label5.grid(row=4, column=0)

    entry1 = tk.Entry(ventana_registro)
    entry1.grid(row=0, column=1)
    entry2 = tk.Entry(ventana_registro)
    entry2.grid(row=1, column=1)
    entry3 = tk.Entry(ventana_registro, show="*")
    entry3.grid(row=2, column=1)
    entry4 = tk.Entry(ventana_registro, show="*")
    entry4.grid(row=3, column=1)

    gm_var = tk.BooleanVar()

    rb_true = tk.Radiobutton(ventana_registro, text="True", variable=gm_var, value=True)
    rb_true.grid(row=4, column=1, sticky="w")
    rb_false = tk.Radiobutton(ventana_registro, text="False", variable=gm_var, value=False)
    rb_false.grid(row=4, column=1, sticky="e")

    boton = tk.Button(ventana_registro, text="Registrarse", command=guardar_datos)
    boton.grid(row=5, column=1)

ventana()
