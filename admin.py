import tkinter as tk
from tkinter import ttk
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
        modificar_button = ttk.Button(frame, text="Modificar")#, command=lambda u=usuario: modificarUsuario(u))
        modificar_button.pack(side=tk.LEFT, padx=5)
        
        # Botón Eliminar
        eliminar_button = ttk.Button(frame, text="Eliminar")#, command=lambda u=usuario: eliminarUsuario(u))
        eliminar_button.pack(side=tk.LEFT)

    usuarios_text.configure(state="disabled")
    
    # Configurar el desplazamiento con la rueda del ratón
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    ventana_usuarios.bind("<MouseWheel>", on_mousewheel)


    
    
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
        es_gm = gm_var.get()  # Obtener el valor del Checkbutton

        if contraseña == confirmar_contraseña:
            documentos = {
                "Nickname": nickname,
                "Correo": correo,
                "Contraseña": contraseña,
                "Confirmar contraseña": confirmar_contraseña,
                "es_gm": es_gm  # Obtener el valor booleano del Checkbutton
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
    gm_var = tk.BooleanVar()  # Variable para almacenar el valor del Checkbutton
    gm_checkbutton = tk.Checkbutton(ventana, text="Es GM", variable=gm_var)
    gm_checkbutton.grid(row=4, column=1)

    # Crear el botón de registro
    boton = tk.Button(ventana, text="Registrarse", command=guardar_datos)
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
