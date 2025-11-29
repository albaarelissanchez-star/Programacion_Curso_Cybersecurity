
# 3. Crea una clase base **Figura** con un método area(). 
# Implementa clases hijas como Círculo y Cuadrado que calculen el área según corresponda.


class Figura:
    def area(self):
        return 0

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        import math
        return math.pi * (self.radio ** 2)

class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado ** 2


if __name__ == "__main__":
    print("\n FIGURAS")
    c1 = Circulo(5)
    cu1 = Cuadrado(4)
    print(f"Área del círculo (radio 5): {c1.area():.2f}")
    print(f"Área del cuadrado (lado 4): {cu1.area()}")

