
# --------------------------------------------
# 4. Crea una clase llamada **CuentaBancaria** con atributos titular y balance. Implementa funciones para depositar y retirar.
# --------------------------------------------

class CuentaBancaria:
    def __init__(self, titular, balance):
        
        self.titular = titular
        self.balance = balance

    def depositar(self, monto):
       
        self.balance += monto
        print(f"Depósito exitoso. Balance actual: {self.balance}")

    def retirar(self, monto):
       
        if monto <= self.balance:
            self.balance -= monto
            print(f"Retiro exitoso. Balance actual: {self.balance}")
        else:
            print("Fondos insuficientes.")


if __name__ == "__main__":
    cuenta = CuentaBancaria("Alba", 500)
    cuenta.depositar(200)
    cuenta.retirar(300)


