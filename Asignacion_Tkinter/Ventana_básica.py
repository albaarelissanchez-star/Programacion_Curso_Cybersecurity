# 1. Crea una ventana básica con Tkinter que muestre un mensaje de bienvenida usando un Label.


import tkinter as tk  # Importamos la biblioteca Tkinter y la renombramos como tk

def main():
    ventana = tk.Tk()

    ventana.title("Bienvenida")

    ventana.geometry("300x150")

    # Creamos un Label (etiqueta) para mostrar el mensaje de bienvenida
    etiqueta_bienvenida = tk.Label(
        ventana,                         # Ventana donde se coloca
        text="¡Bienvenido a Tkinter!",   # Texto a mostrar
        font=("Arial", 14)               # Tipo y tamaño de letra
    )

    # Ubicamos el Label en la ventana usando pack (centrado por defecto)
    etiqueta_bienvenida.pack(pady=40)  # pady añade espacio vertical

    # Iniciamos el bucle principal de la interfaz gráfica
    ventana.mainloop()


# Punto de entrada del programa
if __name__ == "__main__":
    main()
