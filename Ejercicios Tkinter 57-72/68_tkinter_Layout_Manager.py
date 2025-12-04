
# Disponer una serie de botones utilizando el Layout Manager de tipo Pack.

import tkinter as tk

ventana = tk.Tk()
ventana.title("tk")
ventana.geometry("300x300")

# Botones en vertical
btn1 = tk.Button(ventana, text="Botón 1")
btn2 = tk.Button(ventana, text="Botón 2")
btn3 = tk.Button(ventana, text="Botón 3")

btn1.pack(fill="x")
btn2.pack(fill="x")
btn3.pack(fill="x")

# Frame para los botones en horizontal
frame_horizontal = tk.Frame(ventana)
frame_horizontal.pack(pady=10)

btn4 = tk.Button(frame_horizontal, text="Botón 4")
btn5 = tk.Button(frame_horizontal, text="Botón 5")
btn6 = tk.Button(frame_horizontal, text="Botón 6")
btn7 = tk.Button(frame_horizontal, text="Botón 7")

btn4.pack(side="left", padx=2)
btn5.pack(side="left", padx=2)
btn6.pack(side="left", padx=2)
btn7.pack(side="left", padx=2)

ventana.mainloop()
