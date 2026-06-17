#include <stdio.h>
void func() { volatile char buf[1024]; buf[0]=1; }
int main() { func(); int* ptr = NULL; *ptr = 1; return 0; }
