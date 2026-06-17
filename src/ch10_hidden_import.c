#include <windows.h>
#include <stdio.h>

typedef int (WINAPI *MessageBoxAFunc)(HWND, LPCSTR, LPCSTR, UINT);

int main() {
    HMODULE hUser32 = LoadLibraryA("user32.dll");
    if (hUser32 == NULL) {
        printf("Failed to load user32.dll\n");
        return 1;
    }

    MessageBoxAFunc MsgBox = (MessageBoxAFunc)GetProcAddress(hUser32, "MessageBoxA");
    if (MsgBox == NULL) {
        printf("Failed to find MessageBoxA\n");
        return 1;
    }

    MsgBox(NULL, "This MessageBox was loaded dynamically!", "Hidden Import", MB_OK);

    FreeLibrary(hUser32);
    return 0;
}
