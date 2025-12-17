
#include <iostream>
#include <string>
#include <limits>
using namespace std;

struct Estudiante {
    string nombre;
    int edad;
    float promedio;
};

int main() {
    Estudiante e[3];

    for (int i = 0; i < 3; i++) {
        cout << "\nEstudiante " << (i + 1) << endl;

        cout << "Nombre: ";
        getline(cin, e[i].nombre);

        cout << "Edad: ";
        cin >> e[i].edad;

        cout << "Promedio: ";
        cin >> e[i].promedio;

        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }

    int idxMejor = 0;
    for (int i = 1; i < 3; i++) {
        if (e[i].promedio > e[idxMejor].promedio) {
            idxMejor = i;
        }
    }

    cout << "\n--- Mejor Promedio ---\n";
    cout << "Nombre: " << e[idxMejor].nombre << endl;
    cout << "Edad: " << e[idxMejor].edad << endl;
    cout << "Promedio: " << e[idxMejor].promedio << endl;

    return 0;
}
