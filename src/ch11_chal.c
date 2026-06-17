#include <stdio.h>
#include <string.h>
int main() { char buf[32]; scanf("%31s", buf); if(strcmp(buf, "Secret123")==0) printf("Access Granted\n"); else printf("Denied\n"); return 0; }
