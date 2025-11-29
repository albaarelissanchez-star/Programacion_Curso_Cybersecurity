
# --------------------------------------------
# Crea una clase llamada **Usuario** con atributos nombre y edad. Implementa una función que muestre los datos del usuario.
# --------------------------------------------


class Usuario:
    def __init__(self, nombre, edad):
        # Constructor que recibe el nombre y la edad
        self.nombre = nombre
        self.edad = edad

    def mostrar_datos(self):
        # Muestra la información del usuario
        print(f"Nombre: {self.nombre}, Edad: {self.edad}")


if __name__ == "__main__":
    u = Usuario("Alba", 23)
    u.mostrar_datos()
