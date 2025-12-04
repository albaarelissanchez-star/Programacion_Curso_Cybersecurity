
# Mostrar en una ventana un control de tipo Combobox con los días de la semana. 
# Cuando se presione un botón actualizar una Label con el día seleccionado.

import tkinter as tk
from tkinter import ttk

def mostrar_dia():
    dia = combo_dias.get()
    lbl_dia.config(text=f"Día seleccionado: {dia}")

ventana = tk.Tk()
ventana.title("Ejercicio 64")
ventana.geometry("300x200")

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

combo_dias = ttk.Combobox(ventana, values=dias, state="readonly")
combo_dias.current(0)  # Día por defecto
combo_dias.pack(pady=10)

btn_mostrar = ttk.Button(ventana, text="Mostrar día", command=mostrar_dia)
btn_mostrar.pack(pady=5)

lbl_dia = ttk.Label(ventana, text="Día seleccionado: ")
lbl_dia.pack(pady=5)

ventana.mainloop()
