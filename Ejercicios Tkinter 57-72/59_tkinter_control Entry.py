
"""Confeccionar una aplicación que permita ingresar un entero por teclado 
y al presionar un botón muestre dicho valor elevado al cuadrado en una Label."""


import tkinter as tk
from tkinter import messagebox


def calcular_cuadrado():
    try:
        n = int(entrada_num.get())
        resultado = n ** 2
        lbl_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar un número entero válido.")

ventana = tk.Tk()
ventana.title("Ejercicio 59")
ventana.geometry("300x150")

tk.Label(ventana, text="Ingrese un entero:").pack(pady=5)
entrada_num = tk.Entry(ventana)
entrada_num.pack(pady=5)

btn_calcular = tk.Button(ventana, text="Calcular cuadrado", command=calcular_cuadrado)
btn_calcular.pack(pady=5)

lbl_resultado = tk.Label(ventana, text="Resultado: ")
lbl_resultado.pack(pady=5)

ventana.mainloop()
