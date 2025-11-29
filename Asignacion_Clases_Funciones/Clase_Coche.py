
# --------------------------------------------
# 3. Crea una clase llamada **Coche** con atributos marca y velocidad. Agrega una función que aumente la velocidad.
# --------------------------------------------

class Coche:
    def __init__(self, marca, velocidad):
        # Constructor que inicializa marca y velocidad actual
        self.marca = marca
        self.velocidad = velocidad

    def aumentar_velocidad(self, extra):
        # Suma la velocidad adicional a la actual
        self.velocidad += extra
        print(f"Velocidad actual del coche {self.marca}: {self.velocidad} km/h")

if __name__ == "__main__":
     c = Coche("Toyota", 80)
     c.aumentar_velocidad(20)