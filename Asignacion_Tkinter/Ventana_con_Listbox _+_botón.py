
# 4. Crea una ventana con un Listbox que muestre una lista de elementos. 
# Agrega un botón para añadir nuevos elementos a la lista.

import tkinter as tk


def agregar_elemento():
    nuevo = entrada_elemento.get().strip()  # Quitamos espacios al inicio y final
    if nuevo:  # Solo agregamos si no está vacío
        lista_elementos.insert(tk.END, nuevo)  # tk.END agrega al final del Listbox
        entrada_elemento.delete(0, tk.END)  # Borramos el texto del Entry


# Ventana principal
ventana = tk.Tk()
ventana.title("Listbox")
ventana.geometry("400x300")

# Label de título
label_titulo = tk.Label(ventana, text="Lista de elementos", font=("Arial", 12))
label_titulo.pack(pady=5)

# Creamos el Listbox y le agregamos algunos elementos por defecto
lista_elementos = tk.Listbox(ventana, width=40, height=8)
lista_elementos.pack(pady=10)

lista_elementos.insert(tk.END, "Elemento 1")
lista_elementos.insert(tk.END, "Elemento 2")
lista_elementos.insert(tk.END, "Elemento 3")

# Entry para escribir el nuevo elemento
entrada_elemento = tk.Entry(ventana, width=30)
entrada_elemento.pack(pady=5)

# Botón para agregar lo escrito en el Entry al Listbox
boton_agregar = tk.Button(ventana, text="Agregar a la lista", command=agregar_elemento)
boton_agregar.pack(pady=5)

# Iniciamos el bucle principal
ventana.mainloop()

