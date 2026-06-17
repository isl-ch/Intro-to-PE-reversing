#include <windows.h>
#include <stdio.h>
int main() { if (IsDebuggerPresent()) printf("Debugger!\n"); return 0; }
