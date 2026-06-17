#include <windows.h>
LONG WINAPI Handler(EXCEPTION_POINTERS *ExceptionInfo) { return EXCEPTION_CONTINUE_SEARCH; }
int main() { AddVectoredExceptionHandler(1, Handler); return 0; }
