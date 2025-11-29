
# --------------------------------------------
# 5. Crea una clase llamada **Estudiante** con nombre y calificaciones. Implementa una función que calcule el promedio.
# --------------------------------------------

class Estudiante:
    def __init__(self, nombre, calificaciones):
        # Constructor recibe nombre y una lista de calificaciones
        self.nombre = nombre
        self.calificaciones = calificaciones

    def calcular_promedio(self):
        # Suma todas las calificaciones y divide entre la cantidad
        if len(self.calificaciones) == 0:
            return 0
        return sum(self.calificaciones) / len(self.calificaciones)


if __name__ == "__main__":
    e = Estudiante("Alba", [90, 95, 91])
    print("Promedio del estudiante:", e.calcular_promedio())