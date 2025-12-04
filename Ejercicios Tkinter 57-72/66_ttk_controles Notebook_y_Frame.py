# Confeccionar una aplicación que muestre un cuaderno con tres pestañas. Los títulos de cada pestaña deben ser 'Button', 'Label' y 'Entry'. 
# Según la pestaña seleccionada mostrar un mensaje informando el objetivo de la clase y un ejemplo de la misma.

import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.title("Ejercicio 66")
ventana.geometry("400x300")

notebook = ttk.Notebook(ventana)
notebook.pack(fill="both", expand=True)

# Pestaña Button
tab_button = ttk.Frame(notebook)
notebook.add(tab_button, text="Button")

lbl_button_info = ttk.Label(tab_button, text="Un Button permite ejecutar una acción al hacer clic.")
lbl_button_info.pack(pady=10)

ejemplo_button = ttk.Button(tab_button, text="Ejemplo de botón")
ejemplo_button.pack(pady=10)

# Pestaña Label
tab_label = ttk.Frame(notebook)
notebook.add(tab_label, text="Label")

lbl_label_info = ttk.Label(tab_label, text="Una Label muestra texto o información al usuario.")
lbl_label_info.pack(pady=10)

ejemplo_label = ttk.Label(tab_label, text="Ejemplo de Label")
ejemplo_label.pack(pady=10)

# Pestaña Entry
tab_entry = ttk.Frame(notebook)
notebook.add(tab_entry, text="Entry")

lbl_entry_info = ttk.Label(tab_entry, text="Un Entry permite ingresar texto de una sola línea.")
lbl_entry_info.pack(pady=10)

ejemplo_entry = ttk.Entry(tab_entry)
ejemplo_entry.pack(pady=10)

ventana.mainloop()
