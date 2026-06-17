#include <stdio.h>

struct UserData {
    int id;
    int role_level;
    char name[32];
};

void process_user(struct UserData* user) {
    if (user->role_level > 5) {
        printf("Admin access granted for %s (ID: %d)\n", user->name, user->id);
    } else {
        printf("Standard user: %s\n", user->name);
    }
}

int main() {
    struct UserData u1 = {1001, 2, "Alice"};
    struct UserData u2 = {1002, 9, "Bob"};
    
    process_user(&u1);
    process_user(&u2);
    
    return 0;
}
