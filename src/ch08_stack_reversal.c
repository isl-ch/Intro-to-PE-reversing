#include <stdio.h>

// We compile this without optimization so the stack frame matches the challenge.
int calculate(int input) {
    int local_var = 0;
    int val = input;
    
    // Some basic math to match the assembly in the chapter
    local_var += val;
    
    return local_var;
}

int main() {
    int res = calculate(42);
    printf("Result: %d\n", res);
    return 0;
}
