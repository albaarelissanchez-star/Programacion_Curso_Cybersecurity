
# Mostrar una ventana y en su interior dos botones y una label. 
# La label muestra inicialmente el valor 1. 
# Cada uno de los botones permiten incrementar o decrementar en uno el contenido de la labe.


import tkinter as tk

def incrementar():
    valor = int(lbl_valor["text"])
    lbl_valor.config(text=str(valor + 1))

def decrementar():
    valor = int(lbl_valor["text"])
    lbl_valor.config(text=str(valor - 1))

ventana = tk.Tk()
ventana.title("Ejercicio 58")
ventana.geometry("300x150")

lbl_valor = tk.Label(ventana, text="1", font=("Arial", 20))
lbl_valor.pack(pady=10)

btn_mas = tk.Button(ventana, text="Incrementar", command=incrementar)
btn_mas.pack(side="left", padx=20)

btn_menos = tk.Button(ventana, text="Decrementar", command=decrementar)
btn_menos.pack(side="right", padx=20)

ventana.mainloop()
