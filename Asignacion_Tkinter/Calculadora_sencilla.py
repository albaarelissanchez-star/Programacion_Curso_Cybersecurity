
# 3. Crea una calculadora sencilla que pueda sumar dos números usando Labels, Entries y Buttons.

import tkinter as tk


def sumar():
    
    try:
        # Obtenemos los valores de los cuadros de texto
        numero1 = float(entrada_num1.get())
        numero2 = float(entrada_num2.get())

        # Realizamos la suma
        resultado = numero1 + numero2

        # Mostramos el resultado en el Label
        etiqueta_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        # Si el usuario escribe algo que no es número, mostramos error
        etiqueta_resultado.config(text="Error: escribe solo números.")


# Ventana principal
ventana = tk.Tk()
ventana.title("Calculadora Suma")
ventana.geometry("350x250")

# Label y Entry para el primer número
label_num1 = tk.Label(ventana, text="Número 1:")
label_num1.pack(pady=5)
entrada_num1 = tk.Entry(ventana)
entrada_num1.pack(pady=5)

# Label y Entry para el segundo número
label_num2 = tk.Label(ventana, text="Número 2:")
label_num2.pack(pady=5)
entrada_num2 = tk.Entry(ventana)
entrada_num2.pack(pady=5)

# Botón para sumar
boton_sumar = tk.Button(ventana, text="Sumar", command=sumar)
boton_sumar.pack(pady=10)

# Label para mostrar el resultado
etiqueta_resultado = tk.Label(ventana, text="Resultado: ")
etiqueta_resultado.pack(pady=10)

# Iniciamos el bucle principal
ventana.mainloop()
