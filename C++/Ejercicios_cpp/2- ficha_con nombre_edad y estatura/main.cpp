
#include <iostream>
#include <string>
using namespace std;

int main() {
    string nombre;
    int edad;
    float estatura;

    cout << "Ingrese su nombre: ";
    getline(cin, nombre);

    cout << "Ingrese su edad: ";
    cin >> edad;

    cout << "Ingrese su estatura (ej: 1.70): ";
    cin >> estatura;

    cout << "\n----- FICHA -----\n";
    cout << "Nombre   : " << nombre << endl;
    cout << "Edad     : " << edad << " anios" << endl;
    cout << "Estatura : " << estatura << " m" << endl;
    cout << "-----------------\n";

    return 0;
}
