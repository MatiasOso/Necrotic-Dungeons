import tkinter as tk
from tkinter import ttk
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

uri = "mongodb+srv://matiasosores:XJLMzLTVcFYc7iCt@tienda.ietwuqs.mongodb.net/?retryWrites=true&w=majority"

def conexion():
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Conexión exitosa")
        db = client.test  # Cambiar a la base de datos correcta
        return db
    except Exception as e:
        print(e)

#------------------------------ VER USUARIOS ------------------------------#
def viewUsers():
    db = conexion()
    usuarios_collection = db['Usuarios']
    usuarios = usuarios_collection.find()

    ventana_usuarios = tk.Toplevel()
    ventana_usuarios.title("Usuarios")
    
    # Crear un Canvas
    canvas = tk.Canvas(ventana_usuarios, width=500)  # Ajusta el ancho según tus necesidades
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Crear un Scrollbar y vincularlo al Canvas
    scrollbar = tk.Scrollbar(ventana_usuarios, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Crear un Frame dentro del Canvas
    usuarios_frame = ttk.Frame(canvas)
    usuarios_frame.pack(fill=tk.BOTH, expand=True)
    
    canvas.create_window((0, 0), window=usuarios_frame, anchor="nw")
    
    # Configurar el desplazamiento del Canvas
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    usuarios_frame.bind("<Configure>", on_frame_configure)

    for usuario in usuarios:
        frame = ttk.Frame(usuarios_frame)
        frame.pack(pady=5)

        usuarios_text = tk.Text(frame, height=4, width=40)
        usuarios_text.pack(side=tk.LEFT)
        
        usuarios_text.insert(tk.END, f"Nickname: {usuario['Nickname']}\n")
        usuarios_text.insert(tk.END, f"Correo: {usuario['Correo']}\n")
        usuarios_text.insert(tk.END, f"Contraseña: {usuario['Contraseña']}\n")
        usuarios_text.insert(tk.END, f"GM: {usuario['es_gm']}\n")
        
        # Botón Modificar
        modificar_button = ttk.Button(frame, text="Modificar", command=lambda u=usuario: editarUsuario(u))
        modificar_button.pack(side=tk.LEFT)
        
        # Botón Eliminar
        eliminar_button = ttk.Button(frame, text="Eliminar", command=lambda u=usuario: eliminarUsuario(u))
        eliminar_button.pack(side=tk.LEFT)

    usuarios_text.configure(state="disabled")
    
    # Configurar el desplazamiento con la rueda del ratón
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    ventana_usuarios.bind("<MouseWheel>", on_mousewheel)

# ------------------------------ editar usuario ---------------------------------#
def editarUsuario(usuario):
    def guardarCambios():
        # Obtener los nuevos valores ingresados en los Entry
        nuevo_nickname = entry1.get()
        nuevo_correo = entry2.get()
        nuevo_contraseña = entry3.get()
        nuevo_es_gm = gm_var.get()

        # Actualizar los datos del usuario en la base de datos
        db = conexion()
        usuarios_collection = db['Usuarios']
        usuarios_collection.update_one(
            {'_id': usuario['_id']},
            {'$set': {'Nickname': nuevo_nickname, 'Correo': nuevo_correo, 'Contraseña': nuevo_contraseña, 'es_gm': nuevo_es_gm}}
        )
        ventana_editar.destroy()  # Cerrar la ventana de edición

    ventana_editar = tk.Toplevel()
    ventana_editar.title("Editar Usuario")

    # Crear los labels
    label1 = tk.Label(ventana_editar, text="Nickname")
    label1.grid(row=0, column=0)
    label2 = tk.Label(ventana_editar, text="Correo")
    label2.grid(row=1, column=0)
    label3 = tk.Label(ventana_editar, text="Contraseña")
    label3.grid(row=2, column=0)
    label4 = tk.Label(ventana_editar, text="Es Game Master")
    label4.grid(row=3, column=0)

    # Crear los Entry y asignar los valores actuales del usuario
    entry1 = tk.Entry(ventana_editar)
    entry1.insert(tk.END, usuario['Nickname'])
    entry1.grid(row=0, column=1)
    entry2 = tk.Entry(ventana_editar)
    entry2.insert(tk.END, usuario['Correo'])
    entry2.grid(row=1, column=1)
    entry3 = tk.Entry(ventana_editar)
    entry3.insert(tk.END, usuario['Contraseña'])
    entry3.grid(row=2, column=1)

    # Crear el Checkbutton para seleccionar si es GM o no
    gm_var = tk.BooleanVar(value=usuario['es_gm'])  # Variable para almacenar el valor del Checkbutton
    gm_checkbutton = tk.Checkbutton(ventana_editar, variable=gm_var)
    gm_checkbutton.grid(row=3, column=1)

    # Crear el botón de guardar cambios
    boton_guardar = tk.Button(ventana_editar, text="Guardar", command=guardarCambios)
    boton_guardar.grid(row=4, column=0, columnspan=2)

    
#------------------------------ eliminar usuario ------------------------------# 
def eliminarUsuario(usuario):
    db = conexion()
    usuarios_collection = db['Usuarios']
    usuarios_collection.delete_one({'_id': usuario['_id']})
    print("Usuario eliminado")
    
    
    
#------------------------------ CREATE GAMEMASTER ------------------------------#
def createGameMaster():
    db = conexion()
    # Función para guardar los datos en la base de datos
    def guardar_datos(): 
        global label5  # Declarar label5 como variable global
        nickname = entry1.get()
        correo = entry2.get()
        contraseña = entry3.get()
        confirmar_contraseña = entry4.get()
        es_gm = bool(gm_var.get())  # Obtener el valor del Checkbutton

        if contraseña == confirmar_contraseña:
            documentos = {
                "_id":  ObjectId(),
                "Nickname": nickname,
                "Correo": correo,
                "Contraseña": contraseña,
                "Confirmar contraseña": confirmar_contraseña,
                "es_gm": bool(es_gm) # Obtener el valor booleano del Checkbutton
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

        elif contraseña != confirmar_contraseña:
            print("Las contraseñas no coinciden")
            label5 = tk.Label(ventana, text="Las contraseñas no coinciden")
            label5.grid(row=5, column=1)
            ventana.after(1000, ocultar_mensaje)
            return

    def verificar_campos():
        nickname = entry1.get()
        correo = entry2.get()
        contraseña = entry3.get()
        confirmar_contraseña = entry4.get()

        if nickname and correo and contraseña and confirmar_contraseña:
            guardar_datos()
        else:
            label6 = tk.Label(ventana, text="Por favor, complete todos los campos.")
            label6.grid(row=6, column=1)
            # eliminar despues de 1 segundo
            label6.after(1000, label6.destroy)
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
    label3 = tk.Label(ventana, text="Repita Contraseña")
    label3.grid(row=3, column=0)
    label4 = tk.Label(ventana, text="Es Game Master")
    label4.grid(row=4, column=0)
    
    # Crear los entrys
    entry1 = tk.Entry(ventana)
    entry1.grid(row=0, column=1)
    entry2 = tk.Entry(ventana)
    entry2.grid(row=1, column=1)
    entry3 = tk.Entry(ventana, show="*")
    entry3.grid(row=2, column=1)
    entry4 = tk.Entry(ventana, show="*")
    entry4.grid(row=3, column=1)  
    
    # Crear el Checkbutton para seleccionar si es GM o no
    gm_var = tk.IntVar()  # Variable para almacenar el valor del Checkbutton
    gm_checkbutton = tk.Checkbutton(ventana, text="Es GM", variable=gm_var)
    gm_checkbutton.grid(row=4, column=1)

    


    # Crear el botón de registro
    boton = tk.Button(ventana, text="Registrarse", command=verificar_campos)
    boton.grid(row=5, column=1)

    ventana.mainloop()


def mainWindow():
    window = tk.Tk()
    window.title("Administration")
    window.geometry("400x300")
    window.resizable(True, True)
    window.configure(background="white")
    
    button1 = tk.Button(window, text="Create Game Master", command=createGameMaster)
    button1.grid(column=0, row=0)

    button2 = tk.Button(window, text="View Users", command=viewUsers)
    button2.grid(column=0, row=1)
    
    button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    button2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
    window.mainloop()

mainWindow()

# HASTA AQUI VA BIEN TAN SOLO FALTARIA ARREGLAR LO DE SI EL USUARIOS ES GM O NO AL MOMENTO DE REGISTRARSE
