#include <stdio.h>
#include <windows.h>
void NTAPI TlsCallback(PVOID DllHandle, DWORD Reason, PVOID Reserved) { if (Reason == DLL_PROCESS_ATTACH) { printf("I ran before main!\n"); } }
PIMAGE_TLS_CALLBACK pTlsCallback __attribute__((section(".CRT$XLB"))) = TlsCallback;
int main() { printf("I am main!\n"); return 0; }
