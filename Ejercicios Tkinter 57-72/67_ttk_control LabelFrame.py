
# Confeccionar una aplicación que muestre dos controles de tipo LabelFrame. 
# En la primera disponer 2 Label, 2 Entry y un Button, en el segundo LabelFrame disponer 3 botones.

import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.title("Ejercicio 67")
ventana.geometry("400x250")

lf1 = ttk.LabelFrame(ventana, text="Datos")
lf1.pack(fill="x", padx=10, pady=10)

lbl1 = ttk.Label(lf1, text="Nombre:")
lbl1.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry1 = ttk.Entry(lf1)
entry1.grid(row=0, column=1, padx=5, pady=5)

lbl2 = ttk.Label(lf1, text="Apellido:")
lbl2.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry2 = ttk.Entry(lf1)
entry2.grid(row=1, column=1, padx=5, pady=5)

btn_guardar = ttk.Button(lf1, text="Guardar")
btn_guardar.grid(row=2, column=0, columnspan=2, pady=10)

lf2 = ttk.LabelFrame(ventana, text="Acciones")
lf2.pack(fill="x", padx=10, pady=10)

btn1 = ttk.Button(lf2, text="Opción 1")
btn2 = ttk.Button(lf2, text="Opción 2")
btn3 = ttk.Button(lf2, text="Opción 3")

btn1.pack(side="left", padx=5, pady=5)
btn2.pack(side="left", padx=5, pady=5)
btn3.pack(side="left", padx=5, pady=5)

ventana.mainloop()
