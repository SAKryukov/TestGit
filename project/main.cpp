#include <iostream>

int main() {
    int x = 11;
    int y = 12;
    int z = x * y;
    std::cout << "Hello, World!" << std::endl;
    std::cout << x << std::endl;
    std::cout << y << std::endl;
    std::cout << z << std::endl;
    std::cout << "Size of pointer: " << 8 * sizeof(void*) << std::endl;
    return 0;
}