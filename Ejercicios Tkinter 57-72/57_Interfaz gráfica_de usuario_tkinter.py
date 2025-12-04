

# Mostrar una ventana y que en su título aparezca el mensaje 'Hola Mundo'.

import tkinter as tk


ventana = tk.Tk()
ventana.title("Hola Mundo")  # Título de la ventana

ventana.geometry("300x200")  # Tamaño opcional

ventana.mainloop()
