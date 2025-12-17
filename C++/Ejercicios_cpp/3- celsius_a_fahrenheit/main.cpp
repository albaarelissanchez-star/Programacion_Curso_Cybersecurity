
#include <iostream>
using namespace std;

int main() {
    float c;
    cout << "Ingrese grados Celsius: ";
    cin >> c;

    float f = (c * 9.0f / 5.0f) + 32.0f;
    cout << c << " C = " << f << " F" << endl;

    return 0;
}

