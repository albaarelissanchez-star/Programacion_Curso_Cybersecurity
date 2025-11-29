
# --------------------------------------------
# 2. Crea una clase llamada **Rectangulo** que reciba base y altura. Implementa una función que calcule el área.
# --------------------------------------------

class Rectangulo:
    def __init__(self, base, altura):
        # Constructor que recibe base y altura del rectángulo
        self.base = base
        self.altura = altura

    def calcular_area(self):
        # Calcula el área multiplicando base por altura
        return self.base * self.altura
       
        
if __name__ == "__main__":
    r = Rectangulo(10, 5)
    print("Área del rectángulo:", r.calcular_area())