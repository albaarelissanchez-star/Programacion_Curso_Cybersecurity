
# Confeccionar una aplicación que muestre un diálogo cuando se seleccione una opción de un menú.
# El dialogo debe solicitar el ingreso de dos enteros que se utilizarán en la ventana principal para redimensionarla.

import tkinter as tk
from tkinter import simpledialog, messagebox

def cambiar_tamano():
    try:
        ancho = simpledialog.askinteger("Ancho", "Ingrese el ancho de la ventana:")
        if ancho is None:
            return
        alto = simpledialog.askinteger("Alto", "Ingrese el alto de la ventana:")
        if alto is None:
            return
        ventana.geometry(f"{ancho}x{alto}")
    except Exception as e:
        messagebox.showerror("Error", "Ocurrió un error al cambiar el tamaño.")

ventana = tk.Tk()
ventana.title("Ventana")
ventana.geometry("400x300")

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_opcion = tk.Menu(barra_menu, tearoff=0)
menu_opcion.add_command(label="Cambiar tamaño", command=cambiar_tamano)
barra_menu.add_cascade(label="Opciones", menu=menu_opcion)

tk.Label(ventana, text="Use el menú 'Opciones' para cambiar el tamaño.").pack(pady=20)

ventana.mainloop()
