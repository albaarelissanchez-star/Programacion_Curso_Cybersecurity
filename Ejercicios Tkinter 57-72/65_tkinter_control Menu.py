
# Confeccionar una aplicación que muestre dos opciones en el menú de barra superior.
# La primer opción despliega un submenú que permita cambiar el color de fondo del formulario y la segunda permita cambiar el tamaño de formulario.

import tkinter as tk

def cambiar_color(color):
    ventana.config(bg=color)

def cambiar_tamano(geom):
    ventana.geometry(geom)

ventana = tk.Tk()
ventana.title("Ejercicio 65")
ventana.geometry("400x300")

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Menú para color de fondo
menu_color = tk.Menu(barra_menu, tearoff=0)
menu_color.add_command(label="Rojo", command=lambda: cambiar_color("red"))
menu_color.add_command(label="Verde", command=lambda: cambiar_color("green"))
menu_color.add_command(label="Azul", command=lambda: cambiar_color("blue"))
barra_menu.add_cascade(label="Color de fondo", menu=menu_color)

# Menú para tamaño
menu_tamano = tk.Menu(barra_menu, tearoff=0)
menu_tamano.add_command(label="Pequeño (300x200)", command=lambda: cambiar_tamano("300x200"))
menu_tamano.add_command(label="Mediano (500x400)", command=lambda: cambiar_tamano("500x400"))
menu_tamano.add_command(label="Grande (700x500)", command=lambda: cambiar_tamano("700x500"))
barra_menu.add_cascade(label="Tamaño", menu=menu_tamano)

ventana.mainloop()
