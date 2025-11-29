
# 2. Crea una clase base **Empleado** con atributos nombre y salario. 
# Crea clases hijas como Gerente y Técnico, cada una con un método calcular_bono() diferente.


class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def calcular_bono(self):
        return 0

class Gerente(Empleado):
    def calcular_bono(self):
        return self.salario * 0.20

class Tecnico(Empleado):
    def calcular_bono(self):
        return self.salario * 0.10

if __name__ == "__main__":
      print("\n EMPLEADOS")
      gerente = Gerente("Alba", 50000)
      tecnico = Tecnico("Luis", 30000)
      print(f"Gerente -> Bono: ${gerente.calcular_bono():.2f}")
      print(f"Técnico -> Bono: ${tecnico.calcular_bono():.2f}")
