#include <stdio.h>

void __attribute__((constructor)) global_constructor() {
    printf("[+] This is the global constructor executing BEFORE main()!\n");
}

int main() {
    printf("[+] This is main() executing!\n");
    return 0;
}
