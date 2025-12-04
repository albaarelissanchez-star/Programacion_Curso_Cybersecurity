
"""Mostrar dos controles de tipo Radiobutton con las etiquetas "Varón" y "Mujer", 
cuando se presione un botón actualizar una Label con el Radiobutton seleccionado."""

import tkinter as tk

def mostrar_seleccion():
    seleccion = genero.get()
    lbl_resultado.config(text=f"Seleccionado: {seleccion}")

ventana = tk.Tk()
ventana.title("Ejercicio 60")
ventana.geometry("300x150")

genero = tk.StringVar(value="Varón")  # Valor por defecto

rd_varon = tk.Radiobutton(ventana, text="Varón", variable=genero, value="Varón")
rd_mujer = tk.Radiobutton(ventana, text="Mujer", variable=genero, value="Mujer")
rd_varon.pack()
rd_mujer.pack()

btn_mostrar = tk.Button(ventana, text="Mostrar selección", command=mostrar_seleccion)
btn_mostrar.pack(pady=5)

lbl_resultado = tk.Label(ventana, text="Seleccionado: ")
lbl_resultado.pack()

ventana.mainloop()
