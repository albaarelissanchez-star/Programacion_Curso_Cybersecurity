
""" Mostrar una ventana y en su interior tres controles de tipo Checkbutton cuyas etiquetas correspondan a distintos lenguajes de programación. 
Cuando se presione un botón mostrar en una Label la cantidad de Checkbutton que se encuentran chequeados."""

import tkinter as tk

def contar_seleccionados():
    cantidad = 0
    if var_python.get():
        cantidad += 1
    if var_java.get():
        cantidad += 1
    if var_csharp.get():
        cantidad += 1
    lbl_resultado.config(text=f"Seleccionados: {cantidad}")

ventana = tk.Tk()
ventana.title("Ejercicio 61")
ventana.geometry("300x200")

var_python = tk.BooleanVar()
var_java = tk.BooleanVar()
var_csharp = tk.BooleanVar()

chk_python = tk.Checkbutton(ventana, text="Python", variable=var_python)
chk_java = tk.Checkbutton(ventana, text="Java", variable=var_java)
chk_csharp = tk.Checkbutton(ventana, text="C#", variable=var_csharp)

chk_python.pack(anchor="w")
chk_java.pack(anchor="w")
chk_csharp.pack(anchor="w")

btn_contar = tk.Button(ventana, text="Contar seleccionados", command=contar_seleccionados)
btn_contar.pack(pady=5)

lbl_resultado = tk.Label(ventana, text="Seleccionados: 0")
lbl_resultado.pack()

ventana.mainloop()
