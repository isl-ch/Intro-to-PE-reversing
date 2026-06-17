#include <stdio.h>
#include <stdlib.h>

int main() {
    int pin;
    
    printf("--- SECURITY SYSTEM ---\n");
    printf("Enter 4-digit PIN: ");
    
    if (scanf("%d", &pin) != 1) {
        printf("Invalid input format.\n");
        return 1;
    }
    
    if (pin == 1337) {
        printf("Success! Welcome Admin.\n");
    } else {
        printf("Failure! Access Denied.\n");
    }
    
    return 0;
}
