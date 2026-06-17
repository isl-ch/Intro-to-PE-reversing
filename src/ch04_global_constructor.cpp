#include <iostream>

class GlobalClass {
public:
    GlobalClass() {
        std::cout << "[+] This is the global constructor executing BEFORE main()!" << std::endl;
    }
};

GlobalClass g_instance;

int main() {
    std::cout << "[+] This is main() executing!" << std::endl;
    return 0;
}
