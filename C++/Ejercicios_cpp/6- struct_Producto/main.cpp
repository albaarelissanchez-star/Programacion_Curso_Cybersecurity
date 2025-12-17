
#include <iostream>
#include <string>
#include <limits>
using namespace std;

struct Producto {
    string nombre;
    float precio;
    int cantidad;
};

int main() {
    Producto p[5];
    double totalInventario = 0.0;

    for (int i = 0; i < 5; i++) {
        cout << "\nProducto " << (i + 1) << endl;

        cout << "Nombre: ";
        getline(cin, p[i].nombre);

        cout << "Precio: ";
        cin >> p[i].precio;

        cout << "Cantidad: ";
        cin >> p[i].cantidad;

        totalInventario += (double)p[i].precio * p[i].cantidad;

        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }

    cout << "\nValor total del inventario: " << totalInventario << endl;
    return 0;
}
