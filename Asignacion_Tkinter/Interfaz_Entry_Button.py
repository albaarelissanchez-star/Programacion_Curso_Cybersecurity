# 2. Crea una interfaz con un Entry y un Button. Al presionar el botón, muestra el texto escrito en el Entry en un Label.

import tkinter as tk


def mostrar_texto():

    texto = entrada_texto.get()        # Obtenemos el contenido del Entry
    etiqueta_resultado.config(text=f"Escribiste: {texto}")  # Actualizamos el Label


# Ventana principal
ventana = tk.Tk()
ventana.title("Entry y Button")
ventana.geometry("400x200")

# Creamos un Label de instrucción
etiqueta_instruccion = tk.Label(ventana, text="Escribe algo y presiona el botón:")
etiqueta_instruccion.pack(pady=10)

# Creamos el Entry donde el usuario escribe
entrada_texto = tk.Entry(ventana, width=40)
entrada_texto.pack(pady=5)

# Creamos el botón que al presionarse llama a la función mostrar_texto
boton_mostrar = tk.Button(ventana, text="Mostrar texto", command=mostrar_texto)
boton_mostrar.pack(pady=10)

# Label donde se mostrará el resultado
etiqueta_resultado = tk.Label(ventana, text="Aquí aparecerá lo que escribas.")
etiqueta_resultado.pack(pady=10)

# Iniciamos el bucle principal
ventana.mainloop()
