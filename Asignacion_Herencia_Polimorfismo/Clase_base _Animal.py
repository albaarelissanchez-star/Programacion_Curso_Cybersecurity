

# 1. Crea una clase base llamada **Animal** con un método hablar(). 
# Luego crea clases hijas como Perro y Gato que sobreescriban el método.


class Animal:
    def hablar(self):
        return "El animal hace un sonido"

class Perro(Animal):
    def hablar(self):
        return "El perro dice: ¡Guau!"

class Gato(Animal):
    def hablar(self):
        return "El gato dice: ¡Miau!"
        

if __name__ == "__main__":
    print("=== 1. HERENCIA ANIMAL ===")
    animales = [Perro(), Gato(), Animal()]
    for a in animales:
        print(a.hablar())