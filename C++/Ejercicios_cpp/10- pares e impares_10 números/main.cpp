
#include <iostream>
using namespace std;

int main() {
    int num;
    int pares = 0, impares = 0;

    cout << "Ingrese 10 numeros:\n";
    for (int i = 1; i <= 10; i++) {
        cout << "Numero " << i << ": ";
        cin >> num;

        if (num % 2 == 0) pares++;
        else impares++;
    }

    cout << "\nPares: " << pares << endl;
    cout << "Impares: " << impares << endl;

    return 0;
}
