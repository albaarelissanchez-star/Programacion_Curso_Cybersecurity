
# 4. 4. Crea una clase **Vehiculo** con un método mover(). 
# Crea clases hijas como Carro y Bicicleta que implementen su propia versión del método.


class Vehiculo:
    def mover(self):
        return "El vehículo se mueve"

class Carro(Vehiculo):
    def mover(self):
        return "El carro avanza con su motor"

class Bicicleta(Vehiculo):
    def mover(self):
        return "La bicicleta avanza al pedalear"


if __name__ == "__main__":
     print("\n VEHÍCULOS")
     v1 = Carro()
     v2 = Bicicleta()
     print(v1.mover())
     print(v2.mover())
