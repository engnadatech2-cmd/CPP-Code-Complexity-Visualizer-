// simple.cpp
// A straightforward file with low complexity.

#include <iostream>
#include <string>

/**
 * Add two integers.
 */
int add(int a, int b) {
    return a + b;
}

/**
 * Greet a user.
 */
void greet(const std::string& name) {
    std::cout << "Hello, " << name << "!\n";
}

int main() {
    greet("World");
    std::cout << add(2, 3) << "\n";
    return 0;
}
