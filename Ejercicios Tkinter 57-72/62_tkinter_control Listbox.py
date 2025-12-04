
# Disponer un Listbox con una serie de nombres de frutas.
# Permitir la selección solo de uno de ellos. 
# Cuando se presione un botón recuperar la fruta seleccionada y mostrarla en una Label.

import tkinter as tk
from tkinter import messagebox


def mostrar_fruta():
    seleccion = lista_frutas.curselection()
    if not seleccion:
        messagebox.showwarning("Atención", "Debe seleccionar una fruta.")
        return
    indice = seleccion[0]
    fruta = lista_frutas.get(indice)
    lbl_fruta.config(text=f"Fruta seleccionada: {fruta}")

ventana = tk.Tk()
ventana.title("Ejercicio 62")
ventana.geometry("300x250")

frutas = ["Manzana", "Banana", "Naranja", "Pera", "Melón", "Fresa"]

lista_frutas = tk.Listbox(ventana, height=6)
for f in frutas:
    lista_frutas.insert(tk.END, f)
lista_frutas.pack(pady=5)

btn_mostrar = tk.Button(ventana, text="Mostrar fruta", command=mostrar_fruta)
btn_mostrar.pack(pady=5)

lbl_fruta = tk.Label(ventana, text="Fruta seleccionada: ")
lbl_fruta.pack(pady=5)

ventana.mainloop()
