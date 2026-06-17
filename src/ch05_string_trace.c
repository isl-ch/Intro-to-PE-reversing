#include <stdio.h>

int check_args(int count) {
    if (count <= 1) {
        printf("Error: No arguments!\n");
        return 1;
    }
    return 0;
}

int main(int argc, char** argv) {
    if (check_args(argc)) {
        return 1;
    }
    printf("Success: Arguments provided.\n");
    return 0;
}
