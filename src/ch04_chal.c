#include <stdio.h>
void __attribute__((constructor)) init() { printf("Global constructor!\n"); }
int main() { printf("Main!\n"); return 0; }
