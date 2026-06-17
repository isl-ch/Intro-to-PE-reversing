#include <windows.h>
typedef int (WINAPI *MBox)(HWND, LPCSTR, LPCSTR, UINT);
int main() { HMODULE h = LoadLibraryA("user32.dll"); MBox m = (MBox)GetProcAddress(h, "MessageBoxA"); if(m) m(0, "Hi", "Hi", 0); return 0; }
