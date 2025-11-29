
# 5. Crea una clase **Dispositivo** con un método encender(). 
# Crea clases hijas como Laptop y Teléfono que sobreescriban el comportamiento del método.


class Dispositivo:
    def encender(self):
        return "El dispositivo se está encendiendo"

class Laptop(Dispositivo):
    def encender(self):
        return "La laptop está iniciando el sistema operativo"

class Telefono(Dispositivo):
    def encender(self):
        return "El teléfono está iniciando Android/iOS"


if __name__ == "__main__":
    print("\n DISPOSITIVOS")
    d1 = Laptop()
    d2 = Telefono()
    print(d1.encender())
    print(d2.encender())
