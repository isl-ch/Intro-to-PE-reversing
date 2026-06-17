#include <windows.h>
#include <wininet.h>
int main() { InternetOpenA("Test", 0, NULL, NULL, 0); return 0; }
