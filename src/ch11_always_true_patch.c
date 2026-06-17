#include <stdio.h>
#include <string.h>

int main() {
    char password[64];
    
    printf("Enter the password: ");
    if (scanf("%63s", password) != 1) {
        return 1;
    }
    
    if (strcmp(password, "Secret123") == 0) {
        printf("Access Granted\n");
    } else {
        printf("Access Denied\n");
    }
    
    return 0;
}
