
#include <iostream>
using namespace std;

int main() {
    int opcion;
    double a, b;

    do {
        cout << "\n--- MENU ---\n";
        cout << "1) Sumar\n";
        cout << "2) Restar\n";
        cout << "3) Multiplicar\n";
        cout << "4) Salir\n";
        cout << "Elija una opcion: ";
        cin >> opcion;

        if (opcion >= 1 && opcion <= 3) {
            cout << "Ingrese dos numeros: ";
            cin >> a >> b;

            if (opcion == 1) cout << "Resultado: " << (a + b) << endl;
            else if (opcion == 2) cout << "Resultado: " << (a - b) << endl;
            else if (opcion == 3) cout << "Resultado: " << (a * b) << endl;
        } else if (opcion != 4) {
            cout << "Opcion invalida.\n";
        }

    } while (opcion != 4);

    cout << "Programa finalizado.\n";
    return 0;
}
