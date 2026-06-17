#include <stdio.h>
#include <stdlib.h>

void process_command(int cmd) {
    switch(cmd) {
        case 10: printf("Executing Action A\n"); break;
        case 11: printf("Executing Action B\n"); break;
        case 12: printf("Executing Action C\n"); break;
        case 13: printf("Executing Action D\n"); break;
        case 14: printf("Executing Action E\n"); break;
        case 15: printf("Executing Action F\n"); break;
        case 16: printf("Executing Action G\n"); break;
        case 17: printf("Executing Action H\n"); break;
        case 18: printf("Executing Action I\n"); break;
        case 19: printf("Executing Action J\n"); break;
        case 20: printf("Executing Action K\n"); break;
        default: printf("Unknown Action\n"); break;
    }
}

int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s <number>\n", argv[0]);
        return 1;
    }
    int cmd = atoi(argv[1]);
    process_command(cmd);
    return 0;
}
