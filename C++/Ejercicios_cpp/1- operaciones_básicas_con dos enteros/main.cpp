
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cout << "Ingrese dos numeros enteros: ";
    cin >> a >> b;

    cout << "Suma: " << (a + b) << endl;
    cout << "Resta: " << (a - b) << endl;
    cout << "Multiplicacion: " << (a * b) << endl;

    if (b != 0) {
        cout << "Division: " << (a / b) << endl; // division entera
    } else {
        cout << "Division: No se puede dividir entre 0." << endl;
    }

    return 0;
}

