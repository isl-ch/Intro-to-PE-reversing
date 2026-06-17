#include <windows.h>
unsigned char sc[] = {0x90, 0x90, 0xc3};
int main() { DWORD old; VirtualProtect(sc, sizeof(sc), PAGE_EXECUTE_READWRITE, &old); void (*f)() = (void*)sc; f(); return 0; }
