
"""En una aduana hay una máquina que sortea las personas cuyo equipaje serán revisados.
La persona selecciona la cantidad de bultos (hacer dicha selección mediante un Spinbox).

Luego se presiona el botón sortear y aparece al lado de este botón una Label de color rojo o verde 
(En caso de ser rojo se revisa su equipaje, en caso de ser verde, no se revisa) Para el sorteo generar un valor aleatorio entre 1 y 3. 
Si se genera un 1 se revisa, si se genera un 2 o 3 no se revisa, mostrar un mensaje de error si el Spinbox tiene un cero."""

import tkinter as tk
from tkinter import messagebox
import random

def sortear():
    try:
        bultos = int(spin_bultos.get())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido.")
        return

    if bultos == 0:
        messagebox.showerror("Error", "La cantidad de bultos no puede ser cero.")
        return

    numero = random.randint(1, 3)  # 1, 2 o 3
    if numero == 1:
        lbl_resultado.config(text="Revisar equipaje", bg="red", fg="white")
    else:
        lbl_resultado.config(text="No se revisa el equipaje", bg="green", fg="white")

ventana = tk.Tk()
ventana.title("Ejercicio 71 - Aduana")
ventana.geometry("350x200")

tk.Label(ventana, text="Cantidad de bultos:").pack(pady=5)
spin_bultos = tk.Spinbox(ventana, from_=0, to=20)
spin_bultos.pack(pady=5)

btn_sortear = tk.Button(ventana, text="Sortear", command=sortear)
btn_sortear.pack(pady=10)

lbl_resultado = tk.Label(ventana, text="", width=30, height=2)
lbl_resultado.pack(pady=10)

ventana.mainloop()
