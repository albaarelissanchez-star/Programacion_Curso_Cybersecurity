
#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Ingrese un numero: ";
    cin >> n;

    cout << "\nTabla del " << n << ":\n";
    for (int i = 1; i <= 12; i++) {
        cout << n << " x " << i << " = " << (n * i) << endl;
    }

    return 0;
}

