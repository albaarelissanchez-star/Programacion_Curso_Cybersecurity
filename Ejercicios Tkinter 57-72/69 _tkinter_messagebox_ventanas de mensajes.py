
# Confeccionar una aplicación que permita ingresar dos valores enteros y al presionar un botón nos muestre la suma en el título de la ventana. 
# Si el operador no ingresa en alguno de los dos controles Entry datos informar mediante un diálogo el error que se está cometiendo.
# Agregar además un menú de opciones que al ser seleccionado nos muestre información del programa.

import tkinter as tk
from tkinter import messagebox


def sumar():
    a = entrada1.get().strip()
    b = entrada2.get().strip()

    if not a or not b:
        messagebox.showerror("Error", "Debe ingresar ambos valores.")
        return

    try:
        n1 = int(a)
        n2 = int(b)
        suma = n1 + n2
        ventana.title(f"Suma: {suma}")
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar solo números enteros.")

def info_programa():
    messagebox.showinfo("Información", "Aplicación: suma de dos enteros.\nHecho en Tkinter.")

ventana = tk.Tk()
ventana.title("Ejercicio 69")
ventana.geometry("350x200")

tk.Label(ventana, text="Valor 1:").pack(pady=5)
entrada1 = tk.Entry(ventana)
entrada1.pack(pady=5)

tk.Label(ventana, text="Valor 2:").pack(pady=5)
entrada2 = tk.Entry(ventana)
entrada2.pack(pady=5)

btn_sumar = tk.Button(ventana, text="Sumar", command=sumar)
btn_sumar.pack(pady=10)

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_opciones = tk.Menu(barra_menu, tearoff=0)
menu_opciones.add_command(label="Información del programa", command=info_programa)
barra_menu.add_cascade(label="Opciones", menu=menu_opciones)

ventana.mainloop()
