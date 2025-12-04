
# Confeccionar un programa que contenga dos controles de tipo ScrolledText. 
# En el primero ingresamos por teclado cualquier texto. 
# Mediante 4 controles de tipo Entry indicar desde que fila y columna hasta que fila 
# y columna extraer caracteres del primer ScrolledText y copiarlos al segundo ScrolledText cuando se presione un botón.


import tkinter as tk
from tkinter import scrolledtext, messagebox


def copiar_rango():
    try:
        fila_desde = int(ent_fila_desde.get())
        col_desde = int(ent_col_desde.get())
        fila_hasta = int(ent_fila_hasta.get())
        col_hasta = int(ent_col_hasta.get())
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar números enteros en todos los campos.")
        return

    # Índices de Tkinter: "fila.columna" (comienzan en 1.0)
    inicio = f"{fila_desde}.{col_desde}"
    fin = f"{fila_hasta}.{col_hasta}"

    try:
        texto = txt_origen.get(inicio, fin)
    except tk.TclError:
        messagebox.showerror("Error", "Rango inválido.")
        return

    txt_destino.delete("1.0", tk.END)
    txt_destino.insert("1.0", texto)

ventana = tk.Tk()
ventana.title("APP-Controles")
ventana.geometry("700x400")

frame_superior = tk.Frame(ventana)
frame_superior.pack(fill="both", expand=True, pady=5)

txt_origen = scrolledtext.ScrolledText(frame_superior, width=40, height=15)
txt_origen.pack(side="left", padx=5, pady=5)

txt_destino = scrolledtext.ScrolledText(frame_superior, width=40, height=15)
txt_destino.pack(side="right", padx=5, pady=5)

frame_inferior = tk.Frame(ventana)
frame_inferior.pack(pady=5)

tk.Label(frame_inferior, text="Fila desde:").grid(row=0, column=0)
ent_fila_desde = tk.Entry(frame_inferior, width=5)
ent_fila_desde.grid(row=0, column=1, padx=5)

tk.Label(frame_inferior, text="Columna desde:").grid(row=0, column=2)
ent_col_desde = tk.Entry(frame_inferior, width=5)
ent_col_desde.grid(row=0, column=3, padx=5)

tk.Label(frame_inferior, text="Fila hasta:").grid(row=1, column=0)
ent_fila_hasta = tk.Entry(frame_inferior, width=5)
ent_fila_hasta.grid(row=1, column=1, padx=5)

tk.Label(frame_inferior, text="Columna hasta:").grid(row=1, column=2)
ent_col_hasta = tk.Entry(frame_inferior, width=5)
ent_col_hasta.grid(row=1, column=3, padx=5)

btn_copiar = tk.Button(frame_inferior, text="Copiar rango", command=copiar_rango)
btn_copiar.grid(row=2, column=0, columnspan=4, pady=10)

ventana.mainloop()
