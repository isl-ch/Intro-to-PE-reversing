#include <windows.h>
#include <wincrypt.h>
int main() { HCRYPTPROV hProv; CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT); return 0; }
