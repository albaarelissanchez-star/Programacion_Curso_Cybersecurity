
# 5. Diseña una interfaz con un Canvas donde el usuario pueda dibujar líneas manteniendo presionado el botón del mouse.

import tkinter as tk

# Variables globales para guardar la última posición del mouse
ultima_x = None
ultima_y = None


def iniciar_dibujo(evento):
    global ultima_x, ultima_y
    ultima_x = evento.x
    ultima_y = evento.y


def dibujar_linea(evento):
    global ultima_x, ultima_y

    # Dibujamos una línea desde la posición anterior a la nueva
    lienzo.create_line(ultima_x, ultima_y, evento.x, evento.y)

    # Actualizamos las coordenadas para el siguiente tramo de línea
    ultima_x = evento.x
    ultima_y = evento.y


# Ventana principal
ventana = tk.Tk()
ventana.title("Canvas para dibujar")
ventana.geometry("500x400")

# Creamos un Canvas (lienzo) donde podremos dibujar
lienzo = tk.Canvas(ventana, bg="white")
lienzo.pack(fill=tk.BOTH, expand=True)

# Asociamos eventos del mouse al Canvas:
# <Button-1>  -> cuando se presiona el botón izquierdo
# <B1-Motion> -> cuando se mueve el mouse con el botón izquierdo presionado
lienzo.bind("<Button-1>", iniciar_dibujo)
lienzo.bind("<B1-Motion>", dibujar_linea)

# Iniciamos el bucle principal
ventana.mainloop()
